import os
import re
import uuid
import httpx
import time
import pickle
import concurrent.futures
from typing import List

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import MultiVectorRetriever
from langchain_core.stores import InMemoryByteStore

from app.rag.pdf_parser import KimiAPIParser
from app.core.llm_factory import get_embeddings
from app.core.llm_factory import get_llm

_RETRIEVER_INSTANCES = {}

def get_retriever(raw_docs_path: str = "data/raw_docs", vector_db_path: str = "data/vector_db/faiss_index"):
    global _RETRIEVER_INSTANCES
    key = (raw_docs_path, vector_db_path)
    if key not in _RETRIEVER_INSTANCES:
        _RETRIEVER_INSTANCES[key] = OmniRetriever(raw_docs_path, vector_db_path)
    return _RETRIEVER_INSTANCES[key]

class OmniRetriever:
    def __init__(self, raw_docs_path: str, vector_db_path: str):
        self.llm = get_llm(model_type="main", temperature=0.0)
        self.cheap_llm = get_llm(model_type="fast", temperature=0.2)
        self.raw_docs_path = os.path.normpath(raw_docs_path)
        self.vector_db_path = os.path.normpath(vector_db_path)
        self.bm25_path = os.path.normpath(f"{vector_db_path}_bm25.pkl")
        self.kv_store_path = os.path.normpath(f"{vector_db_path}_kv_store.pkl")

        self.parser = KimiAPIParser(output_dir=os.path.join(self.raw_docs_path, "..", "raw_docs_parsed"))

        print("⏳ 正在连接云端免费 Embedding 模型 API (SiliconFlow)...")
        self.embeddings = get_embeddings()

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
        lines = table_content.strip().split('\n')
        safe_table = table_content
        if len(table_content) > 3500 and len(lines) > 2:
            col_count = max(1, lines[0].count('|') - 1)
            safe_table = '\n'.join([lines[0], lines[1], lines[2], "|" + " ... |" * col_count])

        prompt = ChatPromptTemplate.from_template(
            "总结以下学术表格的核心对比关系或关键结论，直接给出总结文字：\n\n{table}"
        )
        chain = prompt | self.llm | StrOutputParser()
        try:
            return chain.invoke({"table": safe_table}).strip()
        except:
            return f"[表格解析兜底] 数据预览: {' '.join(lines[:3])}..."

    async def aingest_documents(self):
        if not os.path.exists(self.raw_docs_path):
            os.makedirs(self.raw_docs_path)
        os.makedirs(os.path.dirname(self.vector_db_path), exist_ok=True)

        pdf_files = [f for f in os.listdir(self.raw_docs_path) if f.endswith('.pdf')]

        if not pdf_files:
            print("⚠️ 未检测到 PDF 文件，初始化空知识库待命...")
            empty_doc = Document(page_content="[空]", metadata={self.id_key: "empty_id", "source": "system"})
            self.vector_store = FAISS.from_documents([empty_doc], self.embeddings)
            self.vector_store.save_local(self.vector_db_path)
            self.bm25_retriever = BM25Retriever.from_documents([empty_doc])
            with open(self.bm25_path, 'wb') as f:
                pickle.dump(self.bm25_retriever, f)
            self.byte_store.mset([("empty_id", b"[empty]")])
            with open(self.kv_store_path, 'wb') as f:
                pickle.dump(self.byte_store.store, f)
            return

        print(f"📚 发现 {len(pdf_files)} 篇文献，开始解析与建库(纯向量+BM25)...")
        vector_docs, store_docs = [], []

        for file in pdf_files:
            file_path = os.path.join(self.raw_docs_path, file)
            # 注意这里使用了之前修复好的 aparse_pdf
            md_file_path = await self.parser.aparse_pdf(file_path)
            with open(md_file_path, "r", encoding="utf-8") as f:
                md_text = f.read()

            elements = self._extract_elements(md_text, file)

            for tb in elements['tables']:
                doc_id = str(uuid.uuid4())
                summary = self._summarize_table(tb["content"])
                vector_docs.append(Document(page_content=summary,
                                            metadata={self.id_key: doc_id, "source": tb["source"], "type": "table"}))
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

        print("✅ 多向量架构持久化完成！")

    def _is_index_outdated(self) -> bool:
        faiss_file = os.path.join(self.vector_db_path, "index.faiss")
        if not os.path.exists(faiss_file):
            return True
        return False

    async def aload_or_build_index(self):
        if self._is_index_outdated():
            await self.aingest_documents()
        else:
            try:
                self.vector_store = FAISS.load_local(self.vector_db_path, self.embeddings,
                                                     allow_dangerous_deserialization=True)
                with open(self.bm25_path, 'rb') as f:
                    self.bm25_retriever = pickle.load(f)
                with open(self.kv_store_path, 'rb') as f:
                    self.byte_store.store = pickle.load(f)
            except:
                await self.aingest_documents()

        if self.vector_store is not None:
            self.multi_retriever = MultiVectorRetriever(vectorstore=self.vector_store, byte_store=self.byte_store,
                                                        id_key=self.id_key)

    async def _rerank_documents(self, query: str, docs: List[Document], top_n: int = 2) -> List[Document]:
        if not docs:
            return []

            # 防御性截断，确保不会超过 API 的单次处理限制（通常是 64 或 128）
        if len(docs) > 64:
            docs = docs[:64]

        api_key = os.getenv("EMBEDDING_API_KEY")
        url = "https://api.siliconflow.cn/v1/rerank"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # 提取纯文本
        doc_texts = [d.page_content if d.page_content.strip() else "Empty Content" for d in docs]

        # 🚨 关键修复点：将 "docs" 改为 "documents"
        payload = {
            "model": "BAAI/bge-reranker-v2-m3",
            "query": query,
            "documents": doc_texts,  # <--- 必须是 documents
            "top_n": top_n,
            "return_documents": False
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, headers=headers, json=payload)

                # 如果还是 400，打印出具体的错误响应体，方便进一步排查
                if response.status_code != 200:
                    print(f"    [❌ Rerank API 报错]: 状态码 {response.status_code}, 内容: {response.text}")
                    return docs[:top_n]

                result = response.json()
                reranked_docs = []
                for item in result.get("results", []):
                    idx = item["index"]
                    docs[idx].metadata["rerank_score"] = item["relevance_score"]
                    reranked_docs.append(docs[idx])

                return reranked_docs
        except Exception as e:
            print(f"    [❌ Rerank 网络异常]: {str(e)}，降级返回原顺序。")
            return docs[:top_n]

    def _compress_document(self, query: str, doc: Document) -> Document | None:
        if len(doc.page_content) < 300: return doc
        prompt = ChatPromptTemplate.from_template("从片段中提取回答【{query}】的核心信息，无关直接回复NONE：\n{context}")
        try:
            summary = (prompt | self.cheap_llm | StrOutputParser()).invoke(
                {"query": query, "context": doc.page_content[:4000]}).strip()
            return None if summary.upper().startswith("NONE") else Document(page_content=f"[提炼] {summary}",
                                                                            metadata=doc.metadata)
        except:
            return Document(page_content=doc.page_content[:1500] + "...", metadata=doc.metadata)

    async def aretrieve(self, query: str, top_k: int = 4) -> List[Document]:
        if self._is_index_outdated():
            self.multi_retriever = None

        if self.multi_retriever is None:
            await self.aload_or_build_index()

        # FAISS & BM25 双路召回
        faiss_sub = self.vector_store.similarity_search(query, k=10)
        bm25_sub = self.bm25_retriever.invoke(query)

        def resolve_docs(sub_docs):
            resolved = []
            for d in sub_docs:
                doc_id = d.metadata.get(self.id_key)
                if doc_id and (raw := self.byte_store.mget([doc_id])[0]):
                    resolved.append(Document(page_content=raw.decode('utf-8'), metadata=d.metadata))
                else:
                    resolved.append(d)
            return resolved

        faiss_docs = resolve_docs(faiss_sub)
        mapped_bm25 = resolve_docs(bm25_sub)

        # ================= 去重与 Rerank =================
        unique_docs_map = {}

        def get_uid(doc):
            return str(doc.metadata.get(self.id_key) or hash(doc.page_content))

        for d in faiss_docs + mapped_bm25:
            uid = get_uid(d)
            if uid not in unique_docs_map:
                unique_docs_map[uid] = d

        candidate_docs = list(unique_docs_map.values())

        # 调用硅基流动接口进行重排序 (保持你之前修复的 documents 传参)
        strict_top_docs = await self._rerank_documents(query, candidate_docs, top_n=top_k)

        # ================= 并行大模型提纯 =================
        compressed_docs = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(strict_top_docs), 5)) as executor:
            future_to_doc = {executor.submit(self._compress_document, query, doc): doc for doc in strict_top_docs}
            for future in concurrent.futures.as_completed(future_to_doc):
                if (comp_doc := future.result()) is not None:
                    compressed_docs.append(comp_doc)

        print(f"    [✨ 提纯完成]: 针对 '{query}' 有效保留 {len(compressed_docs)} 段核心证据。")
        if not compressed_docs and strict_top_docs:
            strict_top_docs[0].page_content = f"[提纯兜底] {strict_top_docs[0].page_content[:1500]}..."
            compressed_docs.append(strict_top_docs[0])

        return compressed_docs