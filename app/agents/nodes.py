import os
import json
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyMuPDFLoader
from app.core.state import AgentState
from app.core.prompts import QUERY_ANALYZER_PROMPT, PEER_REVIEWER_PROMPT
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
        return {"sub_questions": result.sub_questions}
    except Exception as e:
        print(f"    [⚠️ 拆解异常]: {e}，回退使用原始问题。")
        return {"sub_questions": [query]}


def adaptive_retriever(state: AgentState) -> Dict[str, Any]:
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
        if retriever._is_index_outdated():
            retriever.load_or_build_index()

    query = state.get("query", "")

    # 这里的 retrieved_docs 已经是经过底层多线程 LLM 提纯后的高价值压缩文档了，无需再次调用 LLM
    retrieved_docs = retriever.retrieve(query, top_k=4)
    print(f"    [知识获取]: 底层向量库已返回并提纯了 {len(retrieved_docs)} 条相关证据。")

    formatted_docs = []

    # 直接组装，不再做二次大模型并发处理，节省 Token 和时间
    for doc in retrieved_docs:
        source = os.path.basename(doc.metadata.get("source", "未知来源"))
        formatted_docs.append({"source": source, "content": doc.page_content})

    print(f"    [节点完成]: 已将 {len(formatted_docs)} 条核心事实证据打包，准备进入评估环节。")
    return {
        "documents": formatted_docs,
        "retrieval_retries": retries + 1
    }


def peer_reviewer(state: AgentState) -> Dict[str, Any]:
    print("--- 节点: Peer_Reviewer (LLM 评估检索质量) ---")
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
        else:
            feedback_signal = f"EVIDENCE_INSUFFICIENT: {result.feedback}"
    except Exception as e:
        print(f"    [⚠️ 审查节点报错]: {e}。触发防崩溃机制，强制放行。")
        feedback_signal = "APPROVED: API返回异常，触发强制放行机制进入生成报告环节。"

    print(f"    [审查意见]: {feedback_signal}")
    return {"review_feedback": feedback_signal}


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