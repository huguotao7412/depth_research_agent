# app/core/state.py
from typing import TypedDict, List, Dict, Any


class AgentState(TypedDict):
    query: str
    domain_config: Dict[str, Any]
    sub_questions: List[str]
    search_queries: List[str]

    # 【修复 1】移除 Annotated 和 operator.add，变为普通的 List
    # 这样每次 retriever 返回新数据时，会直接覆盖掉上一轮的垃圾数据
    documents: List[Dict[str, Any]]

    review_feedback: str
    retrieval_retries: int
    final_report: str