import os
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.core.state import AgentState
from app.core.prompts import QUERY_ANALYZER_PROMPT, PEER_REVIEWER_PROMPT
from app.rag.retrievers import OmniRetriever  # 【新增】引入真实的多路召回器
from dotenv import load_dotenv

load_dotenv()  # 确保环境变量加载
_retriever_cache = {}
# --- 1. 初始化 LLM ---
llm = ChatOpenAI(model="deepseek-chat", temperature=0)


# --- 2. 定义大模型的结构化输出 Schema ---

class SubQuestionsOutput(BaseModel):
    sub_questions: List[str] = Field(description="拆解出的具体检索子问题列表")


class ReviewerOutput(BaseModel):
    is_sufficient: bool = Field(description="当前文献上下文是否足以回答问题")
    feedback: str = Field(description="如果不足，具体缺少什么信息？如果充足，简述原因。")


# --- 3. 完整节点逻辑 (Nodes) ---

def domain_configurator(state: AgentState) -> Dict[str, Any]:
    """加载目标领域的术语库和数据库配置"""
    print("--- 节点: Domain_Configurator (加载领域配置) ---")

    # 直接获取上游 (API) 传入的配置，如果没传则给个底层的 fallback
    config = state.get("domain_config", {})

    dynamic_config = {
        "domain": config.get("domain", "通用学术领域"),
        "raw_docs_path": config.get("raw_docs_path", "data/raw_docs"),
        "vector_db_path": config.get("vector_db_path", "data/vector_db/faiss_index"),
        "glossary": config.get("glossary", [])
    }

    # 打印出来确认当前加载的领域
    print(f"    [当前领域]: {dynamic_config['domain']}")

    return {"domain_config": dynamic_config, "retrieval_retries": 0, "documents": []}


def query_analyzer(state: AgentState) -> Dict[str, Any]:
    """意图拆解与子问题生成 (接入 LLM)"""
    print("--- 节点: Query_Analyzer (LLM 拆解查询) ---")
    query = state.get("query", "")
    domain_config = state.get("domain_config", {})

    chain = QUERY_ANALYZER_PROMPT | llm.with_structured_output(SubQuestionsOutput, method="function_calling")

    result = chain.invoke({
        "domain": domain_config.get("domain", "通用领域"),
        "glossary": ", ".join(domain_config.get("glossary", [])),
        "query": query
    })

    print(f"    [LLM 拆解结果]: {result.sub_questions}")
    return {"sub_questions": result.sub_questions}


def adaptive_retriever(state: AgentState) -> Dict[str, Any]:
    """跨数据源执行真实的 Agentic RAG"""
    retries = state.get("retrieval_retries", 0)
    print(f"--- 节点: Adaptive_Retriever (执行真实检索, 当前重试次数: {retries}) ---")

    domain_config = state.get("domain_config", {})
    raw_docs_path = domain_config.get("raw_docs_path", "data/raw_docs")
    vector_db_path = domain_config.get("vector_db_path", "data/vector_db/faiss_index")

    global _retriever_cache
    cache_key = f"{raw_docs_path}_{vector_db_path}"

    if cache_key not in _retriever_cache:
        retriever = OmniRetriever(raw_docs_path=raw_docs_path, vector_db_path=vector_db_path)
        retriever.load_or_build_index()
        _retriever_cache[cache_key] = retriever
    else:
        retriever = _retriever_cache[cache_key]
        # 🚨 修复关键：即使命中了内存缓存中的对象，也要让它自检一下文献是否在硬盘上被更新了
        if retriever._is_index_outdated():
            print("🔄 检测到硬盘文献有更新，触发热重载...")
            retriever.load_or_build_index()
        else:
            print("⚡ 命中内存缓存，且文献库未发生改变。")

    query = state.get("query", "")
    retrieved_docs = retriever.retrieve(query, top_k=4)

    formatted_docs = []
    for doc in retrieved_docs:
        source = os.path.basename(doc.metadata.get("source", "未知来源"))
        clean_content = doc.page_content.replace('\n', ' ')
        formatted_docs.append({"source": source, "content": clean_content})

    print(f"    [成功抓取]: 从本地库抓取到 {len(formatted_docs)} 个真实文献片段。")
    return {
        "documents": formatted_docs,
        "retrieval_retries": retries + 1
    }


def peer_reviewer(state: AgentState) -> Dict[str, Any]:
    """事实性检查与抗幻觉 (接入 LLM)"""
    print("--- 节点: Peer_Reviewer (LLM 评估检索质量) ---")
    query = state.get("query", "")
    docs = state.get("documents", [])

    context_str = "\n\n".join([f"来源: {d.get('source', '未知')}\n内容: {d.get('content', '')}" for d in docs])

    chain = PEER_REVIEWER_PROMPT | llm.with_structured_output(ReviewerOutput, method="function_calling")

    result = chain.invoke({
        "query": query,
        "context": context_str if context_str else "暂无检索到的文献。"
    })

    if result.is_sufficient:
        feedback_signal = f"APPROVED: {result.feedback}"
    else:
        feedback_signal = f"EVIDENCE_INSUFFICIENT: {result.feedback}"

    print(f"    [LLM 审查意见]: {feedback_signal}")
    return {"review_feedback": feedback_signal}


# 【新增】撰写报告的独立 Prompt
REPORT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """你是一个严谨的学术报告撰写专家。
请基于下方提供的【文献上下文】，为用户的【研究问题】撰写一份结构化的深度研究报告。

要求：
1. 逻辑清晰，分点阐述。
2. 绝不能凭空捏造，每一项关键结论都必须在句子末尾标明来源，格式为：(来源: xxx.pdf)。
3. 使用 Markdown 语法进行排版。"""),
    ("user", "研究问题: {query}\n\n文献上下文:\n{context}")
])


def report_compiler(state: AgentState) -> Dict[str, Any]:
    """基于真实的文献组装带有引用格式的报告 (接入 LLM)"""
    print("--- 节点: Report_Compiler (LLM 生成最终报告) ---")
    query = state.get("query", "")
    docs = state.get("documents", [])

    context_str = "\n\n".join([f"来源: {d.get('source', '未知')}\n内容: {d.get('content', '')}" for d in docs])

    chain = REPORT_PROMPT | llm

    result = chain.invoke({
        "query": query,
        "context": context_str if context_str else "暂无参考内容"
    })

    print("    [报告生成完毕！]")
    return {"final_report": result.content}