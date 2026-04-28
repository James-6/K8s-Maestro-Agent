# 🚀 K8s-Maestro-Agent: Enterprise Multi-Agent Microservices Platform

![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
![Architecture](https://img.shields.io/badge/Architecture-LangGraph%20%2B%20Multi--Agent-orange.svg)
![Database](https://img.shields.io/badge/Database-PostgreSQL-blue.svg)
![Status](https://img.shields.io/badge/Status-Production_Ready-success.svg)

K8s-Maestro-Agent 是一个基于有向无环图（DAG）状态流转的企业级多智能体协同架构。它彻底抛弃了单体 Agent 的局限性，采用 Supervisor-Workers 模式，专门针对极具复杂度的 Java 微服务体系（如应用商店核心服务、动态流量路由等）提供代码级分析、容器化演进以及深度的生产环境智能排障。

---

## 🏗️ 核心系统架构 (System Architecture)

系统采用 LangGraph 思想构建状态机，实现多个垂类专家 Agent 的上下文共享与长链推理。

```mermaid
graph TD
    User((Developer/DevOps)) -->|自然语言指令 / Webhook告警| Supervisor[Supervisor Agent<br>意图识别与任务路由]
    
    subgraph MigrationSquad [迁移与构建集群]
        Supervisor -->|路由: 容器化改造| CodeAgent[Java AST Analyzer<br>分析业务逻辑与依赖]
        CodeAgent --> YAMLGen[K8s Manifest Generator<br>推算 Request/Limit]
    end

    subgraph DiagnosticSquad [智能诊断集群]
        Supervisor -->|路由: 线上排障| PromAgent[PromQL Expert<br>获取尖刺指标]
        Supervisor -->|路由: 线上排障| LogAgent[ELK Log Parser<br>提取异常堆栈]
        Supervisor -->|路由: 线上排障| PGAgent[PostgreSQL Tuner<br>分析慢查询/死锁]
        
        PromAgent --> Merge[状态机上下文合并]
        LogAgent --> Merge
        PGAgent --> Merge
    end
    
    subgraph Optimization [性能调优]
        Merge --> JVMAgent[JVM Memory Profiler<br>分析 OOM/GC 根因]
    end

    YAMLGen --> Output[产出物 & 修复建议]
    JVMAgent --> Output
    
    Output -->|格式化为 Markdown 卡片| Feishu[Feishu Bot Webhook<br>企微/飞书推送]
    
    %% RAG 知识库增强
    RAG[(历史排障向量库<br>Milvus/Qdrant)] -.->|检索相似故障| Supervisor
