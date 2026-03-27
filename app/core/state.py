from typing import TypedDict, List, Dict, Any, Annotated
import operator


class AgentState(TypedDict):
    """
    OmniResearch-Agent 的核心状态定义
    贯穿整个 LangGraph 工作流的数据结构
    """

    # 1. 用户初始输入
    query: str

    # 2. 领域配置 (由 Domain_Configurator 注入)
    # 例如：{"domain": "雷达医学", "glossary": {...}, "vector_db_path": "..."}
    domain_config: Dict[str, Any]

    # 3. 意图拆解后的子问题列表 (由 Query_Analyzer 生成)
    sub_questions: List[str]

    search_queries: List[str]

    # 4. 检索到的文献上下文 (由 Adaptive_Retriever 执行 Agentic RAG)
    # 使用 operator.add 意味着后续步骤如果触发重新检索，新的 context 会被追加而不是覆盖
    documents: Annotated[List[Dict[str, Any]], operator.add]

    # 5. 审查反馈 (由 Peer_Reviewer 交叉比对后生成)
    # 用于记录事实性检查结果或指出当前 evidence 的不足
    review_feedback: str

    # 6. 状态控制信号
    # 用于控制 Reviewer 回退到 Retriever 的最大次数，防止图陷入死循环
    retrieval_retries: int

    # 7. 最终报告 (由 Report_Compiler 组装)
    final_report: str