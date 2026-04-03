# app/core/state.py
import operator
from typing import Annotated, Sequence, TypedDict, List
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from protocols.a2a.schemas import AgentRole, AgentTaskInstruction


class ResearchState(TypedDict):
    # 核心对话与执行历史
    messages: Annotated[Sequence[BaseMessage], add_messages]

    # 原始查询及配置参数 (新增路径配置)
    user_query: str
    raw_docs_path: str  # <--- 新增
    vector_db_path: str  # <--- 新增

    # A2A 协议控制字段
    next: AgentRole
    current_instruction: AgentTaskInstruction

    # 共享的工作区
    research_plan: Annotated[List[str], operator.add]
    collected_data: Annotated[List[dict], operator.add]
    review_comments: Annotated[List[str], operator.add]
    final_draft: str