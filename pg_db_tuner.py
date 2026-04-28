from langchain_core.tools import tool

@tool
def analyze_pg_stat_activity() -> str:
    """查询 PostgreSQL pg_stat_activity 系统视图，检查锁等待和空闲长事务。"""
    # 模拟执行 SQL: SELECT pid, state, wait_event_type, query FROM pg_stat_activity WHERE state = 'active';
    return """
    [Alert] 发现 45 个连接处于 'active' 状态。
    Wait Event: ClientRead
    Query snippet: UPDATE app_metrics SET download_score = ... WHERE id = ...
    Diagnosis: 微服务未正确释放 PG 连接，导致连接池满。并非 MySQL 的表锁问题，而是 PG 特有的长事务占用 Slot。
    """
