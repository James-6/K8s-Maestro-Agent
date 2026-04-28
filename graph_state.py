from typing import TypedDict, Annotated, Sequence, Optional
import operator
from langchain_core.messages import BaseMessage

class MaestroState(TypedDict):
    """
    定义多 Agent 协作的全局状态 (State)。
    每次 Agent 执行完毕后，都会将结果 Merge 到这个状态中，传递给下一个 Agent。
    """
    messages: Annotated[Sequence[BaseMessage], operator.add]
    
    # 告警上下文
    alert_source: str           # e.g., "Prometheus", "Feishu_Webhook"
    target_pod: Optional[str]   # 发生异常的 K8s Pod 名称
    namespace: str              # K8s 命名空间
    
    # 诊断收集到的结构化数据
    jvm_heap_usage: Optional[float]
    pg_active_connections: Optional[int]
    pg_deadlocks_detected: bool
    
    # 路由控制
    next_node: str              # 下一个应该执行的 Agent 节点名称
    is_resolved: bool           # 故障是否已定位完毕
    
    # 最终输出的修复建议报告
    diagnostic_report: Optional[str]
