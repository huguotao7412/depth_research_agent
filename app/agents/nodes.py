import os
import json
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyMuPDFLoader  # 【新增】用于读取 PDF 进行领域嗅探
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


# 【新增】用于自动嗅探领域的大模型输出结构
class DomainExtractionOutput(BaseModel):
    domain: str = Field(description="该文献所属的具体学术领域，例如：'毫米波雷达医学监测'或'高分子可降解材料'")
    glossary: List[str] = Field(description="从文献中提取的5-8个核心专业术语/英文缩写")


# --- 3. 完整节点逻辑 (Nodes) ---

def _is_config_outdated(target_dir: str, cache_file: str) -> bool:
    """检查缓存的领域配置是否过期（是否有新的 PDF 加入）"""
    if not os.path.exists(cache_file):
        return True
    cache_mtime = os.path.getmtime(cache_file)
    if os.path.exists(target_dir):
        for f in os.listdir(target_dir):
            if f.endswith('.pdf'):
                # 如果有任何 PDF 的修改时间晚于配置文件的生成时间，说明文献换了
                if os.path.getmtime(os.path.join(target_dir, f)) > cache_mtime:
                    return True
    return False


def domain_configurator(state: AgentState) -> Dict[str, Any]:
    """智能加载或自动嗅探目标领域的术语库和配置"""
    print("--- 节点: Domain_Configurator (自动领域嗅探) ---")

    target_data_dir = "data/raw_docs"
    cache_file = os.path.join(target_data_dir, "auto_domain_config.json")

    dynamic_config = {
        "domain": "通用学术领域",
        "raw_docs_path": target_data_dir,
        "vector_db_path": "data/vector_db/faiss_index",
        "glossary": []
    }

    if not os.path.exists(target_data_dir):
        os.makedirs(target_data_dir)

    # 1. 如果缓存没过期，直接使用缓存（省 Token）
    if not _is_config_outdated(target_data_dir, cache_file):
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                local_config = json.load(f)
                dynamic_config.update(local_config)
            print(f"    [⚡ 命中领域缓存]: 当前领域 -> {dynamic_config['domain']}")
            return {"domain_config": dynamic_config, "retrieval_retries": 0, "documents": []}
        except Exception:
            pass

    # 2. 如果过期或不存在，触发 LLM 自动嗅探
    pdf_files = [f for f in os.listdir(target_data_dir) if f.endswith('.pdf')]
    if not pdf_files:
        print("    [警告]: 目录下没有 PDF 文件，使用通用领域设置")
        return {"domain_config": dynamic_config, "retrieval_retries": 0, "documents": []}

    print("    [🔍 触发自动嗅探]: 检测到新文献，正在阅读并提取领域和关键词...")
    first_pdf_path = os.path.join(target_data_dir, pdf_files[0])

    try:
        # 提取第一篇文献的前两页文本
        loader = PyMuPDFLoader(first_pdf_path)
        docs = loader.load()
        sample_text = "\n".join([doc.page_content for doc in docs[:2]])

        # 呼叫 LLM 自动总结领域和关键词
        extraction_prompt = ChatPromptTemplate.from_messages([
            ("system",
             "你是一个资深的学术情报分析师。请阅读以下文献片段，总结出它所属的【具体学术领域】，并提取5-8个【核心学术术语】。"),
            ("user", "文献片段:\n{text}")
        ])

        chain = extraction_prompt | llm.with_structured_output(DomainExtractionOutput, method="function_calling")
        # 限制字数防止 token 溢出
        result = chain.invoke({"text": sample_text[:2000]})

        dynamic_config["domain"] = result.domain
        dynamic_config["glossary"] = result.glossary

        # 将大模型提取的结果保存下来，下次直接读取
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump({
                "domain": result.domain,
                "glossary": result.glossary
            }, f, ensure_ascii=False, indent=2)

        print(f"    [✅ 自动提取成功]: 领域 -> {result.domain}")
        print(f"    [✅ 核心关键词]: {', '.join(result.glossary)}")

    except Exception as e:
        print(f"    [自动提取失败]: {e}，将使用通用领域设置")

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
    """跨数据源执行真实的 Agentic RAG (支持热重载)"""
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
            print("🔄 检测到硬盘文献有更新，触发知识库热重载...")
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


# 撰写报告的独立 Prompt
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