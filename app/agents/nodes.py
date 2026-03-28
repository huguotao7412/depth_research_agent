import os
import json
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.tools.tavily_search import TavilySearchResults
from app.core.state import AgentState
from app.core.prompts import QUERY_ANALYZER_PROMPT, PEER_REVIEWER_PROMPT, REPORT_PROMPT
from app.rag.retrievers import OmniRetriever
from dotenv import load_dotenv
load_dotenv()

_retriever_cache = {}

# --- 1. 初始化 LLM ---
llm = ChatOpenAI(model="deepseek-chat", temperature=0)


# --- 2. 定义大模型的结构化输出 Schema ---
class SubQuestionsOutput(BaseModel):
    sub_questions: List[str] = Field(description="拆解出的具体检索子问题列表")


class ReviewerOutput(BaseModel):
    is_sufficient: bool = Field(description="当前文献上下文是否足以回答问题")
    feedback: str = Field(description="如果不足，具体缺少什么信息？如果充足，简述原因。")
    # 【新增】大模型反思后的新关键词字段
    suggested_queries: List[str] = Field(default=[],
                                         description="如果证据不足，提供的2-3个建议重新检索的同义关键词或查询短句")


class DomainExtractionOutput(BaseModel):
    domain: str = Field(description="该文献所属的具体学术领域，例如：'毫米波雷达医学监测'或'高分子可降解材料'")
    glossary: List[str] = Field(description="从文献中提取的5-8个核心专业术语/英文缩写")


# --- 3. 完整节点逻辑 (Nodes) ---

def _is_config_outdated(target_dir: str, cache_file: str) -> bool:
    if not os.path.exists(cache_file):
        return True
    cache_mtime = os.path.getmtime(cache_file)
    if os.path.exists(target_dir):
        for f in os.listdir(target_dir):
            if f.endswith('.pdf'):
                if os.path.getmtime(os.path.join(target_dir, f)) > cache_mtime:
                    return True
    return False


def domain_configurator(state: AgentState) -> Dict[str, Any]:
    print("--- 节点: Domain_Configurator (自动领域嗅探) ---")
    target_data_dir = "data/raw_docs"
    cache_file = os.path.join(target_data_dir, "auto_domain_config.json")
    dynamic_config = {"domain": "通用学术领域", "raw_docs_path": target_data_dir,
                      "vector_db_path": "data/vector_db/faiss_index", "glossary": []}

    if not os.path.exists(target_data_dir):
        os.makedirs(target_data_dir)

    if not _is_config_outdated(target_data_dir, cache_file):
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                local_config = json.load(f)
                dynamic_config.update(local_config)
            print(f"    [⚡ 命中领域缓存]: 当前领域 -> {dynamic_config['domain']}")
            return {"domain_config": dynamic_config, "retrieval_retries": 0, "documents": []}
        except Exception:
            pass

    pdf_files = [f for f in os.listdir(target_data_dir) if f.endswith('.pdf')]
    if not pdf_files:
        return {"domain_config": dynamic_config, "retrieval_retries": 0, "documents": []}

    print("    [🔍 触发自动嗅探]: 检测到新文献，正在阅读并提取领域和关键词...")
    first_pdf_path = os.path.join(target_data_dir, pdf_files[0])

    try:
        loader = PyMuPDFLoader(first_pdf_path)
        docs = loader.load()
        sample_text = "\n".join([doc.page_content for doc in docs[:2]])

        extraction_prompt = ChatPromptTemplate.from_messages([
            ("system",
             "你是一个资深的学术情报分析师。请阅读以下文献片段，总结出它所属的【具体学术领域】，并提取5-8个【核心学术术语】。"),
            ("user", "文献片段:\n{text}")
        ])

        chain = extraction_prompt | llm.with_structured_output(DomainExtractionOutput, method="function_calling")
        result = chain.invoke({"text": sample_text[:2000]})

        dynamic_config["domain"] = result.domain
        dynamic_config["glossary"] = result.glossary

        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump({"domain": result.domain, "glossary": result.glossary}, f, ensure_ascii=False, indent=2)

        print(f"    [✅ 自动提取成功]: 领域 -> {result.domain}")
    except Exception as e:
        print(f"    [自动提取失败]: {e}，将使用通用领域设置")

    return {"domain_config": dynamic_config, "retrieval_retries": 0, "documents": []}


def query_analyzer(state: AgentState) -> Dict[str, Any]:
    print("--- 节点: Query_Analyzer (LLM 拆解查询) ---")
    query = state.get("query", "")
    domain_config = state.get("domain_config", {})

    chain = QUERY_ANALYZER_PROMPT | llm.with_structured_output(SubQuestionsOutput, method="function_calling")
    try:
        result = chain.invoke({
            "domain": domain_config.get("domain", "通用领域"),
            "glossary": ", ".join(domain_config.get("glossary", [])),
            "query": query
        })
        print(f"    [LLM 拆解结果]: {result.sub_questions}")
        return {"sub_questions": result.sub_questions,
                "search_queries": result.sub_questions}
    except Exception as e:
        print(f"    [⚠️ 拆解异常]: {e}，回退使用原始问题。")
        return {"sub_questions": [query]}


def adaptive_retriever(state: AgentState) -> Dict[str, Any]:
    """跨数据源执行真实的 Agentic RAG (支持热重载与多路查询)"""
    retries = state.get("retrieval_retries", 0)
    print(f"--- 节点: Adaptive_Retriever (执行真实检索, 当前重试次数: {retries}) ---")

    domain_config = state.get("domain_config", {})
    raw_docs_path = domain_config.get("raw_docs_path", "data/raw_docs")
    vector_db_path = domain_config.get("vector_db_path", "data/vector_db/faiss_index")

    global _retriever_cache
    cache_key = f"{raw_docs_path}_{vector_db_path}"

    # 1. 初始化或热加载向量库
    if cache_key not in _retriever_cache:
        retriever = OmniRetriever(raw_docs_path=raw_docs_path, vector_db_path=vector_db_path)
        retriever.load_or_build_index()
        _retriever_cache[cache_key] = retriever
    else:
        retriever = _retriever_cache[cache_key]
        if retriever._is_index_outdated():
            print("🔄 检测到硬盘文献有更新，触发知识库热重载...")
            retriever.load_or_build_index()
        else:
            print("⚡ 命中内存缓存，且文献库未发生改变。")

    # 2. 【核心修改】获取当前活动的检索词列表
    queries_to_search = state.get("search_queries", [])
    if not queries_to_search:
        # 如果由于某种原因状态机里没有 search_queries，兜底使用原始 query
        queries_to_search = [state.get("query", "")]

    formatted_docs = []
    seen_sources = set()  # 用来对不同关键词召回的内容做简单去重

    # 3. 针对每一个子问题/新关键词进行并发或循环检索
    for q in queries_to_search:
        print(f"    [🔍 正在检索]: {q}")
        # 每个子问题找 Top 2 就够了，避免合并后把大模型上下文撑爆
        retrieved_docs = retriever.retrieve(q, top_k=2)

        for doc in retrieved_docs:
            source = os.path.basename(doc.metadata.get("source", "未知来源"))
            clean_content = doc.page_content.replace('\n', ' ')

            # 使用内容哈希进行文本去重，防止不同检索词召回同一段高频文字
            content_hash = hash(clean_content)
            if content_hash not in seen_sources:
                seen_sources.add(content_hash)
                formatted_docs.append({"source": source, "content": clean_content})

    print(f"    [成功抓取]: 根据当前策略，抓取并去重得到 {len(formatted_docs)} 个文献片段。")
    return {
        "documents": formatted_docs,
        "retrieval_retries": retries + 1
    }


def peer_reviewer(state: AgentState) -> Dict[str, Any]:
    """事实性检查与抗幻觉，附带自我反思重写 (接入 LLM)"""
    print("--- 节点: Peer_Reviewer (LLM 评估检索质量与反思) ---")
    query = state.get("query", "")
    docs = state.get("documents", [])

    context_str = "\n\n".join([f"来源: {d.get('source', '未知')}\n内容: {d.get('content', '')}" for d in docs])

    chain = PEER_REVIEWER_PROMPT | llm.with_structured_output(ReviewerOutput, method="function_calling")

    try:
        result = chain.invoke({
            "query": query,
            "context": context_str if context_str else "暂无检索到的文献。"
        })

        if result.is_sufficient:
            feedback_signal = f"APPROVED: {result.feedback}"
            new_search_queries = []  # 审查通过，不需要新的检索词了
        else:
            feedback_signal = f"EVIDENCE_INSUFFICIENT: {result.feedback}"
            new_search_queries = result.suggested_queries  # 【核心修改】提取大模型反思后的新关键词
            print(f"    [💡 触发反思机制]: 建议下一轮使用新关键词检索 -> {new_search_queries}")

    except Exception as e:
        print(f"    [⚠️ 审查节点报错]: {e}。触发防崩溃机制，强制放行。")
        # 即使 API 报错，也强制兜底通过，保证能够生成最终报告
        feedback_signal = "APPROVED: API返回异常，触发强制放行机制进入生成报告环节。"
        new_search_queries = []

    print(f"    [LLM 审查意见]: {feedback_signal}")

    # 【核心修改】将新的检索词传回状态机，覆盖之前的 search_queries
    return {
        "review_feedback": feedback_signal,
        "search_queries": new_search_queries
    }


def report_compiler(state: AgentState) -> Dict[str, Any]:
    print("--- 节点: Report_Compiler (LLM 生成最终报告) ---")
    query = state.get("query", "")
    docs = state.get("documents", [])

    context_str = "\n\n".join([f"来源: {d.get('source', '未知')}\n内容: {d.get('content', '')}" for d in docs])
    chain = REPORT_PROMPT | llm

    try:
        result = chain.invoke({
            "query": query,
            "context": context_str if context_str else "暂无参考内容"
        })
        final_content = result.content
    except Exception as e:
        final_content = f"⚠️ 生成报告时发生网络或 API 错误: {str(e)}"

    print("    [报告生成完毕！]")
    return {"final_report": final_content}


def external_academic_search(state: AgentState) -> Dict[str, Any]:
    """旁路节点：当本地文献库无法回答时，触发 Tavily 外部 Web 搜索"""
    print("--- 节点: External_Academic_Search (Tavily 联网检索旁路) ---")

    # 提取评审专家在上一步打回时给出的建议检索词，兜底用原问题
    queries_to_search = state.get("search_queries", [])
    if not queries_to_search:
        queries_to_search = [state.get("query", "")]

    # 初始化 Tavily 搜索工具
    tavily_tool = TavilySearchResults(max_results=3)

    web_docs = []
    seen_urls = set()

    for q in queries_to_search:
        print(f"    [🌐 正在呼叫外援检索]: {q}")
        try:
            # 执行全网搜索
            results = tavily_tool.invoke({"query": q})
            for res in results:
                url = res.get("url", "未知网页")
                content = res.get("content", "")

                if url not in seen_urls and content:
                    seen_urls.add(url)
                    # 强行打上 Web 标签，让大模型在写报告时明确标出 (来源: [Web] URL)
                    web_docs.append({
                        "source": f"[Web] {url}",
                        "content": f"[外部联网补充信息] {content}"
                    })
        except Exception as e:
            print(f"    [⚠️ Tavily 检索异常]: {e}")

    print(f"    [外援到达]: 从互联网成功补充了 {len(web_docs)} 条外部高价值参考信息。")

    # 因为 state.py 中的 documents 标注了 operator.add
    # 这里返回的 web_docs 会被无缝追加到之前本地检索的文档列表中，不会覆盖！
    return {"documents": web_docs}