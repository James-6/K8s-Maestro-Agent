from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from graph_state import MaestroState

@tool
def check_k8s_oom_events(pod_name: str, namespace: str) -> str:
    """查询指定 Pod 过去 1 小时的 Kubernetes OOMKilled 事件和 dmesg 日志。"""
    # 模拟实际调用 kubernetes-client
    return f"Pod {pod_name} terminated with Reason: OOMKilled. Exit Code: 137. Last dmesg context: Memory cgroup out of memory."

@tool
def fetch_java_heap_dump_summary(pod_name: str) -> str:
    """获取应用崩溃前的堆内存快照摘要（通过 Prometheus jvm_memory_bytes_used 指标分析）。"""
    # 这里结合了极其具体的业务场景：动态域名替换服务
    if "webfilter" in pod_name:
        return """
        Heap Analysis Summary:
        - 85% of Old Gen is occupied by byte[] arrays.
        - Dominator Tree shows these are originating from HTTP Response Body parsing threads.
        - Warning: No upper limit cache eviction policy detected for large payload caching.
        """
    return "Heap usage normal."

class JVMMemoryProfiler:
    def __init__(self, llm: ChatOpenAI):
        self.tools = [check_k8s_oom_events, fetch_java_heap_dump_summary]
        prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个 Java 性能调优与 K8s 容器化专家。
            你需要深入排查由于内存泄漏或不当缓存导致的 OOM 问题。
            注意：在处理动态代理或网关类服务时，必须检查响应体缓存策略，警惕大对象撑爆内存，必须强制要求引入上限缓存策略 (Upper Limit Cache)。"""),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])
        agent = create_tool_calling_agent(llm, self.tools, prompt)
        self.executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)

    def invoke(self, state: MaestroState) -> dict:
        target_pod = state["target_pod"]
        result = self.executor.invoke({
            "input": f"分析 Pod {target_pod} 的内存状态，确定是否发生 OOM 并给出代码级优化建议。"
        })
        
        # 将分析结果写入状态机的报告中
        return {"diagnostic_report": result["output"], "is_resolved": True}
