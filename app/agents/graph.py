from langgraph.graph import StateGraph, START, END
from app.core.state import AgentState
from app.agents.nodes import (
    domain_configurator,
    query_analyzer,
    adaptive_retriever,
    peer_reviewer,
    report_compiler
)
from app.agents.edges import check_retrieval_quality


def build_omni_research_graph():
    # 1. 实例化状态图
    workflow = StateGraph(AgentState)

    # 2. 添加节点
    workflow.add_node("Domain_Configurator", domain_configurator)
    workflow.add_node("Query_Analyzer", query_analyzer)
    workflow.add_node("Adaptive_Retriever", adaptive_retriever)
    workflow.add_node("Peer_Reviewer", peer_reviewer)
    workflow.add_node("Report_Compiler", report_compiler)

    # 3. 定义标准执行流 (边)
    workflow.add_edge(START, "Domain_Configurator")
    workflow.add_edge("Domain_Configurator", "Query_Analyzer")
    workflow.add_edge("Query_Analyzer", "Adaptive_Retriever")
    workflow.add_edge("Adaptive_Retriever", "Peer_Reviewer")

    # 4. 定义条件路由边 (核心逻辑：从 Reviewer 出发)
    workflow.add_conditional_edges(
        "Peer_Reviewer",
        check_retrieval_quality,
        {
            "re_retrieve": "Adaptive_Retriever",
            "compile_report": "Report_Compiler"
        }
    )

    # 5. 结束流
    workflow.add_edge("Report_Compiler", END)

    # 6. 编译并返回可执行的 app
    return workflow.compile()