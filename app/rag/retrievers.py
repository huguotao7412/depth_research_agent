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
        prompt = ChatPromptTemplate.from_template(
            "总结以下学术表格的核心对比关系或关键结论，直接给出总结文字：\n\n{table}"
        )
        chain = prompt | self.llm | StrOutputParser()
        try:
            return chain.invoke({"table": table_content[:3500]}).strip()
        except Exception as e:
            lines = table_content.split('\n')
            return f"数据表格预览: {' '.join(lines[:3])}"

    def ingest_documents(self):
        if not os.path.exists(self.raw_docs_path):
            os.makedirs(self.raw_docs_path)
            return
        pdf_files = [f for f in os.listdir(self.raw_docs_path) if f.endswith('.pdf')]
        if not pdf_files:
            return

        vector_docs = []
        store_docs = []

        for file in pdf_files:
            file_path = os.path.join(self.raw_docs_path, file)
            md_file_path = self.parser.parse_pdf(file_path)
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

    def load_or_build_index(self):
        if not self._is_index_outdated():
            print("🚀 正在从硬盘加载多向量索引...")
            self.vector_store = FAISS.load_local(self.vector_db_path, self.embeddings,
                                                 allow_dangerous_deserialization=True)
            with open(self.bm25_path, 'rb') as f:
                self.bm25_retriever = pickle.load(f)
            with open(self.kv_store_path, 'rb') as f:
                self.byte_store.store = pickle.load(f)
            self.multi_retriever = MultiVectorRetriever(vectorstore=self.vector_store, byte_store=self.byte_store,
                                                        id_key=self.id_key)
        else:
            self.ingest_documents()
            self.multi_retriever = MultiVectorRetriever(vectorstore=self.vector_store, byte_store=self.byte_store,
                                                        id_key=self.id_key)

    def _compress_document(self, query: str, doc: Document) -> Document | None:
        """使用 LLM 动态抽取长文档中与当前查询真正相关的核心信息"""
        # 如果文本很短，不需要浪费 Token 压缩，直接返回
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

        # 为了防止撑爆上下文，送入压缩大模型前最多截断到前 4000 字符
        chain = prompt | self.llm | StrOutputParser()
        try:
            summary = chain.invoke({"query": query, "context": doc.page_content[:4000]}).strip()

            # 如果大模型判定无关，返回 None 以丢弃该文档
            if summary.upper().startswith("NONE") or summary == "NONE":
                return None

            # 组装压缩后的新文档，原封不动保留来源元数据
            compressed_content = f"[基于大模型信息提炼] {summary}"
            return Document(page_content=compressed_content, metadata=doc.metadata)

        except Exception as e:
            print(f"⚠️ 文档动态压缩失败，回退为原始截断文本: {e}")
            return Document(page_content=doc.page_content[:1500] + "\n...(内容因过长被截断)", metadata=doc.metadata)

    def retrieve(self, query: str, top_k: int = 4) -> List[Document]:
        if self.multi_retriever is None:
            self.load_or_build_index()

        # ==================== 核心修复 ====================
        # 手动执行 FAISS 检索并解码 byte_store，绕过 MultiVectorRetriever 的强制 JSON 解析
        faiss_sub_docs = self.vector_store.similarity_search(query)
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
        # =================================================

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

        # RRF 融合打分
        c = 60
        scores = {}
        doc_map = {}
        for rank, d in enumerate(mapped_bm25):
            h = d.page_content
            doc_map[h] = d
            scores[h] = scores.get(h, 0) + 1 / (rank + c)
        for rank, d in enumerate(faiss_docs):
            h = d.page_content
            doc_map[h] = d
            scores[h] = scores.get(h, 0) + 1 / (rank + c)

        # 截取融合后排名最高的 Top K 篇“原始长文档”
        sorted_res = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        raw_top_docs = [doc_map[content] for content, score in sorted_res[:top_k]]

        # --- 并行 LLM 压缩与二次过滤 (保留在底层处理) ---
        print(f"🔍 针对子问题 '{query}'，召回 {len(raw_top_docs)} 段长文本，正在进行 LLM 并行压缩与提纯...")
        compressed_docs = []

        # 使用多线程加速处理
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(top_k, 4)) as executor:
            future_to_doc = {executor.submit(self._compress_document, query, doc): doc for doc in raw_top_docs}

            for future in concurrent.futures.as_completed(future_to_doc):
                comp_doc = future.result()
                if comp_doc is not None:
                    compressed_docs.append(comp_doc)

        print(f"✨ 提纯完成，有效保留 {len(compressed_docs)} 段高价值压缩证据。")
        return compressed_docs