# app/agents/graph.py
from langgraph.graph import StateGraph, END, START
from app.core.state import ResearchState
from app.agents.supervisor import create_supervisor_node
# 假设你已经在 workers 目录下实现了这些节点函数
from app.agents.workers.planner import planner_node
from app.agents.workers.researcher import researcher_node
from app.agents.workers.reviewer import reviewer_node
from app.agents.workers.writer import writer_node
from app.agents.workers.daily_qa import daily_qa_node

def build_multi_agent_graph(llm):
    workflow = StateGraph(ResearchState)

    # 1. 添加所有的节点
    workflow.add_node("Supervisor", create_supervisor_node(llm))
    workflow.add_node("Planner", planner_node)
    workflow.add_node("Researcher", researcher_node)
    workflow.add_node("Reviewer", reviewer_node)
    workflow.add_node("Writer", writer_node)
    workflow.add_node("DailyQA", daily_qa_node)

    # 2. 所有的 Worker 节点完成后，必须回到 Supervisor 汇报工作
    workflow.add_edge("Planner", "Supervisor")
    workflow.add_edge("Researcher", "Supervisor")
    workflow.add_edge("Reviewer", "Supervisor")
    workflow.add_edge("Writer", "Supervisor")
    workflow.add_edge("DailyQA", "Supervisor")

    # 3. 定义 Supervisor 的条件路由边
    # 它会根据 state["next"] 的值自动路由到对应的 Worker 节点或结束
    workflow.add_conditional_edges(
        "Supervisor",
        lambda state: state["next"],
        {
            "Planner": "Planner",
            "Researcher": "Researcher",
            "Reviewer": "Reviewer",
            "Writer": "Writer",
            "DailyQA": "DailyQA",
            "FINISH": END
        }
    )

    # 4. 设置入口点
    workflow.add_edge(START, "Supervisor")

    return workflow.compile()