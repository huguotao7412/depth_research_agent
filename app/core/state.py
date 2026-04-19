# app/core/state.py
import operator
from typing import Annotated, Sequence, TypedDict, List, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from protocols.a2a.schemas import AgentRole, AgentTaskInstruction
from pydantic import BaseModel

class Instruction(BaseModel):
    task_description: str

class ResearchState(TypedDict):
    # ==========================================
    # 1. 核心对话与短期记忆 (Core & Memory)
    # ==========================================
    messages: Annotated[Sequence[BaseMessage], add_messages]
    session_summary: str      # 短期会话情境摘要 (防爆机制提炼的记忆)
    workspace_id: str         # 当前工作区 ID (物理与记忆隔离凭证)

    # ==========================================
    # 2. 物理存储路径 (Storage Paths)
    # ==========================================
    raw_docs_path: str        # 当前工作区的 PDF 存放路径
    vector_db_path: str       # 当前工作区的 FAISS 索引存放路径

    # ==========================================
    # 3. 智能体流转控制 (Agent Routing)
    # ==========================================
    next: AgentRole           # 决定下一步路由给哪个 Agent
    current_instruction: Optional[Instruction] # 传递给当前 Agent 的具体执行指令

    # ==========================================
    # 4. 共享工作台 (Shared Workspace Variables)
    # ==========================================
    research_plan: List[str]  # Planner 拆解的并发子任务大纲
    collected_data: List[dict] # Researcher 并发收集的证据汇总 (直接覆盖，不跨轮累加)
    review_comments: List[str] # Reviewer 的审查打回意见 (直接覆盖，不跨轮累加)
    final_draft: str          # Writer 生成的最终报告初稿