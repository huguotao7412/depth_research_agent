# app/agents/graph.py
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver # 🚨 引入内置持久化记忆库
from app.core.state import ResearchState
from app.agents.supervisor import create_supervisor_node
from app.agents.workers.planner import planner_node
from app.agents.workers.researcher import researcher_node
from app.agents.workers.reviewer import reviewer_node
from app.agents.workers.writer import writer_node
from app.agents.workers.daily_qa import daily_qa_node
from app.agents.workers.memory_manager import memory_manager_node # 🚨 引入新写的记忆节点

def build_multi_agent_graph(llm):
    workflow = StateGraph(ResearchState)

    # 1. 添加所有的节点
    workflow.add_node("Supervisor", create_supervisor_node(llm))
    workflow.add_node("Planner", planner_node)
    workflow.add_node("Researcher", researcher_node)
    workflow.add_node("Reviewer", reviewer_node)
    workflow.add_node("Writer", writer_node)
    workflow.add_node("DailyQA", daily_qa_node)
    workflow.add_node("MemoryManager", memory_manager_node) # 🚨 注册记忆节点

    # 2. 所有的 Worker 节点完成后，必须回到 Supervisor 汇报工作
    workflow.add_edge("Planner", "Supervisor")
    workflow.add_edge("Researcher", "Supervisor")
    workflow.add_edge("Reviewer", "Supervisor")
    workflow.add_edge("Writer", "Supervisor")
    workflow.add_edge("DailyQA", "Supervisor")

    workflow.add_edge(START, "Supervisor")

    # 3. 定义 Supervisor 的条件路由边
    workflow.add_conditional_edges(
        "Supervisor",
        lambda state: state["next"],
        {
            "Planner": "Planner",
            "Researcher": "Researcher",
            "Reviewer": "Reviewer",
            "Writer": "Writer",
            "DailyQA": "DailyQA",
            "FINISH": "MemoryManager"  # 🚨 核心拦截：原先直接结束的，现在交给记忆引擎处理
        }
    )

    # 🚨 记忆管理节点处理完成后，才真正结束图流转
    workflow.add_edge("MemoryManager", END)

    # 🚨 挂载内置 Checkpointer，真正实现跨请求的会话记忆连贯性
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)