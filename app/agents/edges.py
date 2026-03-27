from app.core.state import AgentState

def check_retrieval_quality(state: AgentState) -> str:
    """
    决定是继续生成报告，打回重新检索，还是触发外部 Web 搜索。
    """
    feedback = state.get("review_feedback", "")
    retries = state.get("retrieval_retries", 0)
    MAX_RETRIES = 3  # 防止死循环

    if "EVIDENCE_INSUFFICIENT" in feedback:
        if retries < MAX_RETRIES:
            print(f"--- 路由: 本地证据不足，打回重审 (当前重试 {retries}/{MAX_RETRIES}) ---")
            return "re_retrieve"
        else:
            print(f"--- 路由: 本地检索已达最大重试次数 ({MAX_RETRIES})，触发旁路 Web 外部搜索 ---")
            return "web_search"
    else:
        print("--- 路由: 证据充足，直接进入 Report_Compiler ---")
        return "compile_report"