from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from graph_state import MaestroState

# 定义路由输出结构
class RouterDecison(BaseModel):
    next_node: str = Field(
        description="The next expert agent to call. Must be one of: 'jvm_expert', 'pg_tuner', 'log_parser', 'feishu_notifier'"
    )
    reason: str = Field(description="Reasoning for routing to this expert.")

class SupervisorAgent:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm.with_structured_output(RouterDecison)
        self.system_prompt = """你是一个 K8s 微服务集群的资深 SRE 和调度架构师。
        你需要根据当前收集到的故障上下文（如 Pod OOM、数据库响应慢等），将任务路由给最合适的专家 Agent。
        - 如果发现内存尖刺或 OOMKilled，路由给 'jvm_expert'。
        - 如果发现数据库连接池满或长事务，路由给 'pg_tuner'。
        - 如果问题已明确，路由给 'feishu_notifier' 发送报告。
        """

    def invoke(self, state: MaestroState) -> dict:
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder(variable_name="messages"),
            ("user", f"Current Pod: {state.get('target_pod')}. JVM Heap: {state.get('jvm_heap_usage')}. PG Connections: {state.get('pg_active_connections')}. Determine next step.")
        ])
        
        chain = prompt | self.llm
        decision: RouterDecison = chain.invoke({"messages": state["messages"]})
        
        # 返回状态更新
        return {"next_node": decision.next_node}
