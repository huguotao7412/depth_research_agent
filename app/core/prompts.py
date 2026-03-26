from langchain_core.prompts import ChatPromptTemplate

# 1. 意图拆解 Prompt (Query Analyzer)
# 动态注入领域专家设定 <Domain_Expertise>
QUERY_ANALYZER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """你是一个资深的学术研究员。当前你的研究领域是：{domain}。
相关的核心术语包括：{glossary}。

你的任务是将用户的宏观研究问题，拆解为 2-3 个具体的、可被检索子问题 (Sub-questions)。
请确保拆解后的问题有助于后续在学术文献数据库中进行关键词或语义检索。"""),
    ("user", "用户问题: {query}")
])

# 2. 事实性检查与评审 Prompt (Peer Reviewer)
# 强制大模型交叉比对检索到的 Context [cite: 22]
PEER_REVIEWER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """你是一个严苛的同行评审专家 (Peer Reviewer)。
你需要评估提供的文献上下文 (Context) 是否足以充分、严谨地回答用户的问题。
决不能凭空捏造 (幻觉)，只能基于提供的 Context 进行评判。

如果证据不足、缺少关键数据或具体算法细节，请给出明确的反馈，并要求重新检索。
如果证据充足，请予以批准。"""),
    ("user", """
用户原始问题: {query}
----------------
当前检索到的文献上下文: 
{context}
----------------
请给出你的评审结果。""")
])