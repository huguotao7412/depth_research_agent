from app.core.state import AgentState


def check_retrieval_quality(state: AgentState) -> str:
    """
    决定是继续生成报告，还是打回重新检索 [cite: 24, 44]。
    """
    feedback = state.get("review_feedback", "")
    retries = state.get("retrieval_retries", 0)
    MAX_RETRIES = 3  # 防止死循环

    if "EVIDENCE_INSUFFICIENT" in feedback and retries < MAX_RETRIES:
        print(f"--- 路由: 证据不足，强制回退到 Retriever (重试 {retries}/{MAX_RETRIES}) ---")
        return "re_retrieve"
    else:
        print("--- 路由: 证据充足或达到最大重试次数，进入 Report_Compiler ---")
        return "compile_report"