import os
import re
import uuid
import time
import pickle
import concurrent.futures
from typing import List

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import MultiVectorRetriever
from langchain_core.stores import InMemoryByteStore

from app.rag.pdf_parser import KimiAPIParser


class OmniRetriever:
    def __init__(self, raw_docs_path: str, vector_db_path: str):
        # 主力模型，用于摘要和压缩，开启重试和较长超时
        self.llm = ChatOpenAI(model="deepseek-chat", temperature=0, max_retries=3, timeout=40)
        self.raw_docs_path = os.path.normpath(raw_docs_path)
        self.vector_db_path = os.path.normpath(vector_db_path)
        self.bm25_path = os.path.normpath(f"{vector_db_path}_bm25.pkl")
        self.kv_store_path = os.path.normpath(f"{vector_db_path}_kv_store.pkl")

        self.parser = KimiAPIParser(output_dir=os.path.join(self.raw_docs_path, "..", "raw_docs_parsed"))

        print("⏳ 正在加载 Embedding 模型...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-zh-v1.5",
            model_kwargs={'device': 'cpu'}
        )
        self.vector_store = None
        self.bm25_retriever = None
        self.multi_retriever = None

        self.byte_store = InMemoryByteStore()
        self.id_key = "doc_id"

    def _extract_elements(self, md_text: str, source_file: str) -> dict:
        elements = {"texts": [], "tables": []}
        table_pattern = r"(?:\|.*\|(?:\n|\r\n?))+"
        tables = re.findall(table_pattern, md_text)
        for tb in tables:
            if len(tb.strip()) > 30:
                elements["tables"].append({"content": tb.strip(), "source": source_file})

        clean_text = re.sub(table_pattern, "\n\n[表格已提取]\n\n", md_text)
        headers_to_split_on = [("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3")]
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        text_splits = markdown_splitter.split_text(clean_text)

        for split in text_splits:
            split.metadata["source"] = source_file
            elements["texts"].append(split)
        return elements

    def _summarize_table(self, table_content: str) -> str:
        time.sleep(0.5)

        def safe_truncate_table(table_str: str, max_len: int = 3500) -> str:
            if len(table_str) <= max_len:
                return table_str

            lines = table_str.strip().split('\n')
            # 如果格式异常，不足2行，回退到普通截断
            if len(lines) <= 2:
                return table_str[:max_len]

            # 强制保留前两行：表头 (Header) 和 分隔符 (Separator, 例如 |---|---|)
            result_lines = [lines[0], lines[1]]
            current_len = len(lines[0]) + len(lines[1]) + 2

            for line in lines[2:]:
                if current_len + len(line) + 1 > max_len:
                    # 当超出长度时，优雅地添加一个省略行，提示大模型表格已截断
                    col_count = max(1, lines[0].count('|') - 1)
                    result_lines.append("|" + " ... |" * col_count)
                    break
                result_lines.append(line)
                current_len += len(line) + 1

            return '\n'.join(result_lines)

        # 预处理获取结构完整的安全表格
        safe_table = safe_truncate_table(table_content)

        prompt = ChatPromptTemplate.from_template(
            "总结以下学术表格的核心对比关系或关键结论，直接给出总结文字：\n\n{table}"
        )
        chain = prompt | self.llm | StrOutputParser()
        try:
            return chain.invoke({"table": safe_table}).strip()
        except Exception as e:
            # 异常兜底也优化一下，保证返回的预览信息更清晰
            lines = table_content.split('\n')
            return f"[表格解析异常兜底] 数据表格预览: {' '.join(lines[:3])}..."

    async def aingest_documents(self):
        # 1. 确保目录一定存在
        if not os.path.exists(self.raw_docs_path):
            os.makedirs(self.raw_docs_path)

        # 确保向量库的父目录也存在 (防止刚 clone 下来没 data/vector_db 文件夹报错)
        os.makedirs(os.path.dirname(self.vector_db_path), exist_ok=True)

        pdf_files = [f for f in os.listdir(self.raw_docs_path) if f.endswith('.pdf')]

        # 2. 【核心修复】为刚 Clone 项目的新用户初始化一个空库，防止后续检索报 None 错误
        if not pdf_files:
            print("⚠️ 未检测到 PDF 文件，初始化空知识库待命...")
            empty_doc = Document(page_content="[知识库当前为空，请挂载文献]",
                                 metadata={self.id_key: "empty_id", "source": "system"})

            self.vector_store = FAISS.from_documents([empty_doc], self.embeddings)
            self.vector_store.save_local(self.vector_db_path)

            self.bm25_retriever = BM25Retriever.from_documents([empty_doc])
            with open(self.bm25_path, 'wb') as f:
                pickle.dump(self.bm25_retriever, f)

            self.byte_store.mset([("empty_id", "[知识库当前为空，请挂载文献]".encode('utf-8'))])
            with open(self.kv_store_path, 'wb') as f:
                pickle.dump(self.byte_store.store, f)
            print("✅ 空知识库初始化完成！")
            return

        # ================= 下方为你原有的正常解析逻辑 =================
        print(f"📚 发现 {len(pdf_files)} 篇文献，开始解析建库...")
        vector_docs = []
        store_docs = []

        for file in pdf_files:
            file_path = os.path.join(self.raw_docs_path, file)
            md_file_path =await self.parser.parse_pdf(file_path)
            with open(md_file_path, "r", encoding="utf-8") as f:
                md_text = f.read()

            elements = self._extract_elements(md_text, file)

            for tb in elements['tables']:
                doc_id = str(uuid.uuid4())
                summary = self._summarize_table(tb["content"])
                summary_doc = Document(page_content=summary,
                                       metadata={self.id_key: doc_id, "source": tb["source"], "type": "table"})
                vector_docs.append(summary_doc)
                store_docs.append((doc_id, tb["content"].encode('utf-8')))

            for txt_doc in elements['texts']:
                doc_id = str(uuid.uuid4())
                txt_doc.metadata[self.id_key] = doc_id
                txt_doc.metadata["type"] = "text"
                vector_docs.append(txt_doc)
                store_docs.append((doc_id, txt_doc.page_content.encode('utf-8')))

        self.vector_store = FAISS.from_documents(vector_docs, self.embeddings)
        self.vector_store.save_local(self.vector_db_path)
        self.byte_store.mset(store_docs)

        with open(self.kv_store_path, 'wb') as f:
            pickle.dump(self.byte_store.store, f)

        self.bm25_retriever = BM25Retriever.from_documents(vector_docs)
        with open(self.bm25_path, 'wb') as f:
            pickle.dump(self.bm25_retriever, f)
        print("✅ 知识库多向量架构已持久化到硬盘！")

    def _is_index_outdated(self) -> bool:
        faiss_file = os.path.join(self.vector_db_path, "index.faiss")
        if not os.path.exists(faiss_file) or not os.path.exists(self.bm25_path) or not os.path.exists(
                self.kv_store_path):
            return True
        index_time = os.path.getmtime(faiss_file)
        for f in os.listdir(self.raw_docs_path):
            if f.endswith('.pdf'):
                if os.path.getmtime(os.path.join(self.raw_docs_path, f)) > index_time:
                    return True
        return False

    async def aload_or_build_index(self):
        # 如果索引过期或者不存在（比如刚 clone 下来的新用户）
        if self._is_index_outdated():
            print("🔄 索引不存在或已过期，触发知识库构建...")
            await self.aingest_documents()
        else:
            print("🚀 正在从硬盘加载多向量索引...")
            try:
                self.vector_store = FAISS.load_local(self.vector_db_path, self.embeddings,
                                                     allow_dangerous_deserialization=True)
                with open(self.bm25_path, 'rb') as f:
                    self.bm25_retriever = pickle.load(f)
                with open(self.kv_store_path, 'rb') as f:
                    self.byte_store.store = pickle.load(f)
            except Exception as e:
                print(f"⚠️ 硬盘索引加载失败 (可能已损坏): {e}，尝试强制重建...")
                await self.aingest_documents()

        # 无论如何，最后一定要挂载 multi_retriever
        if self.vector_store is not None:
            self.multi_retriever = MultiVectorRetriever(
                vectorstore=self.vector_store,
                byte_store=self.byte_store,
                id_key=self.id_key
            )

    # ================= 新增：HyDE 假设性文档生成器 =================
    def _generate_hyde_document(self, query: str) -> str:
        """调用 LLM 生成假设性学术回答，用于跨越语义鸿沟"""
        prompt = ChatPromptTemplate.from_template(
            "你是一个资深的学术专家。请针对下面的【检索问题】，写一段简短的学术回答（约100-200字）。\n\n"
            "⚠️ 严格要求：\n"
            "1. 你不需要保证内容的绝对事实正确性，但请务必在回答中尽可能多地堆叠该领域相关的【专业术语】、【常用指标】、【算法简称】或【核心概念】。\n"
            "2. 不要包含任何寒暄或解释性的话语（如“这个问题指的是...”），直接输出学术段落本体，这段文本将直接送入向量数据库进行匹配。\n\n"
            "检索问题: {query}\n\n"
            "假设性学术回答:"
        )
        try:
            chain = prompt | self.llm | StrOutputParser()
            # 极速生成，消耗极低 Token
            hyde_doc = chain.invoke({"query": query}).strip()
            return hyde_doc
        except Exception as e:
            print(f"    [⚠️ HyDE 生成失败]: {e}，回退使用原始 query。")
            return query

    # =========================================================

    def _compress_document(self, query: str, doc: Document) -> Document | None:
        """使用 LLM 动态抽取长文档中与当前查询真正相关的核心信息"""
        if len(doc.page_content) < 300:
            return doc

        prompt = ChatPromptTemplate.from_template(
            "你是一个学术信息提取专家。请阅读以下参考文档片段，并从中提取出能够回答或关联到【用户问题】的精确信息、数据和结论。\n\n"
            "要求：\n"
            "1. 尽可能保留原始数值、算法名称和核心逻辑。\n"
            "2. 如果该文档片段与用户问题【完全无关】，请直接回复大写字母：NONE。\n"
            "3. 只输出提取出的有用信息，不附加任何寒暄。\n\n"
            "用户问题：{query}\n\n"
            "参考文档片段：\n{context}"
        )

        chain = prompt | self.llm | StrOutputParser()
        try:
            summary = chain.invoke({"query": query, "context": doc.page_content[:4000]}).strip()
            if summary.upper().startswith("NONE") or summary == "NONE":
                return None
            compressed_content = f"[基于大模型信息提炼] {summary}"
            return Document(page_content=compressed_content, metadata=doc.metadata)

        except Exception as e:
            print(f"⚠️ 文档动态压缩失败，回退为原始截断文本: {e}")
            return Document(page_content=doc.page_content[:1500] + "\n...(内容因过长被截断)", metadata=doc.metadata)

    async def aretrieve(self, query: str, top_k: int = 4) -> List[Document]:
        if self.multi_retriever is None:
            await self.aload_or_build_index()

        # --- 1. 触发 HyDE 机制 ---
        print(f"    [🧠 触发 HyDE]: 正在为 '{query}' 实时生成假设性学术回答以增强语义检索...")
        hypothetical_doc = self._generate_hyde_document(query)
        # print(f"    [HyDE 内容]: {hypothetical_doc[:50]}...") # 调试时可解开注释看假答案长什么样

        # --- 2. FAISS 语义检索 (注入 HyDE 假设性文档) ---
        faiss_sub_docs = self.vector_store.similarity_search(hypothetical_doc)
        faiss_docs = []
        for d in faiss_sub_docs:
            doc_id = d.metadata.get(self.id_key)
            if doc_id:
                raw = self.byte_store.mget([doc_id])[0]
                if raw:
                    faiss_docs.append(Document(page_content=raw.decode('utf-8'), metadata=d.metadata))
                else:
                    faiss_docs.append(d)
            else:
                faiss_docs.append(d)

        # --- 3. BM25 关键词检索 (保留原始短 query 防止噪音) ---
        bm25_docs = self.bm25_retriever.invoke(query)
        mapped_bm25 = []
        for d in bm25_docs:
            doc_id = d.metadata.get(self.id_key)
            if doc_id:
                raw = self.byte_store.mget([doc_id])[0]
                if raw:
                    mapped_bm25.append(Document(page_content=raw.decode('utf-8'), metadata=d.metadata))
                else:
                    mapped_bm25.append(d)
            else:
                mapped_bm25.append(d)

        # --- 4. RRF 融合打分 (修复 Hash 覆盖漏洞) ---
        c = 60
        scores = {}
        doc_map = {}

        # 定义一个辅助函数获取唯一的 document ID
        def get_unique_id(doc: Document) -> str:
        # 优先获取入库时生成的 UUID，如果由于某种原因缺失，则使用内容+元数据的混合哈希作为唯一标识
            doc_id = doc.metadata.get(self.id_key)
            if doc_id:
                        return str(doc_id)
            return str(hash(doc.page_content + doc.metadata.get("source", "unknown")))

        # 计算 BM25 召回得分
        for rank, d in enumerate(mapped_bm25):
                    uid = get_unique_id(d)
                    doc_map[uid] = d
                    scores[uid] = scores.get(uid, 0) + 1 / (rank + c)

        # 计算 FAISS 语义召回得分
        for rank, d in enumerate(faiss_docs):
                    uid = get_unique_id(d)
                    doc_map[uid] = d
                    scores[uid] = scores.get(uid, 0) + 1 / (rank + c)

        # 依据 RRF 综合得分倒序排列
        sorted_res = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        raw_top_docs = [doc_map[uid] for uid, score in sorted_res[:top_k]]

        # --- 5. 并行 LLM 压缩与二次过滤 ---
        print(f"    [🔍 过滤提纯]: 召回 {len(raw_top_docs)} 段长文本，正在多线程提取核心证据...")
        compressed_docs = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(top_k, 4)) as executor:
            future_to_doc = {executor.submit(self._compress_document, query, doc): doc for doc in raw_top_docs}

            for future in concurrent.futures.as_completed(future_to_doc):
                comp_doc = future.result()
                if comp_doc is not None:
                    compressed_docs.append(comp_doc)

        print(f"    [✨ 提纯完成]: 针对 '{query}' 有效保留了 {len(compressed_docs)} 段核心证据。")

        if not compressed_docs and raw_top_docs:
            print(f"    [⚠️ 防断链兜底触发]: 提纯模型认为召回结果均无关。强制保留 RRF 粗排 Top 1 供审查...")
            fallback_doc = raw_top_docs[0]
            # 打上特殊标记，截断防超长，让下游 Reviewer 知道这是没经过提纯的次优数据
            fallback_doc.page_content = f"[提纯阶段判定无关的兜底原始数据] {fallback_doc.page_content[:1500]}..."
            compressed_docs.append(fallback_doc)
        return compressed_docs