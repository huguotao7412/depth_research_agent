import os
import re
import uuid
import pickle
from typing import List

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever

# --- 多向量检索核心组件 ---
# PyCharm 如果在这里报红，请直接忽略，运行时会自动解析
from langchain_classic.retrievers import MultiVectorRetriever
from langchain_core.stores import InMemoryByteStore
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 引入基于 API 的解析器
from app.rag.pdf_parser import KimiAPIParser


class OmniRetriever:
    def __init__(self, raw_docs_path: str, vector_db_path: str):
        self.raw_docs_path = raw_docs_path
        self.vector_db_path = vector_db_path
        self.bm25_path = f"{vector_db_path}_bm25.pkl"

        # 新增：用于存储完整 Markdown 表格和长文本的本地 KV 数据库路径
        self.kv_store_path = f"{vector_db_path}_kv_store"

        # 初始化 API 解析器
        self.parser = KimiAPIParser(output_dir=f"{raw_docs_path}_parsed")

        print("⏳ 正在加载 Embedding 模型...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-zh-v1.5",
            model_kwargs={'device': 'cpu'}
        )
        self.vector_store = None
        self.bm25_retriever = None
        self.multi_retriever = None

        # 初始化本地文件存储，用于存放多向量的底层原始数据
        self.byte_store = InMemoryByteStore()
        self.id_key = "doc_id"

    def _extract_elements(self, md_text: str, source_file: str) -> dict:
        """利用正则从 Markdown 中分离出纯文本和表格"""
        elements = {"texts": [], "tables": []}

        # 1. 提取 Markdown 表格 (匹配包含 | 的连续行)
        table_pattern = r"(?:\|.*\|(?:\n|\r\n?))+"
        tables = re.findall(table_pattern, md_text)
        for tb in tables:
            # 过滤掉偶然匹配出的太短的假表格
            if len(tb.strip()) > 30:
                elements["tables"].append({"content": tb.strip(), "source": source_file})

        # 2. 剥离表格后的纯文本
        clean_text = re.sub(table_pattern, "\n\n[表格已提取]\n\n", md_text)

        # 3. 对纯文本按标题层级切分
        headers_to_split_on = [("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3")]
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        text_splits = markdown_splitter.split_text(clean_text)

        for split in text_splits:
            split.metadata["source"] = source_file
            elements["texts"].append(split)

        return elements

    def _summarize_table(self, table_content: str) -> str:
        """调用 DeepSeek 为表格生成语义摘要，便于 FAISS 被精准命中"""
        llm = ChatOpenAI(model="deepseek-chat", temperature=0)
        prompt = ChatPromptTemplate.from_template(
            "你是一个资深的学术助手。请用一段连贯的中文文字，总结以下 Markdown 表格的【核心内容、对比关系或关键数据结论】，以便于后续进行语义向量检索。\n\n表格内容：\n{table}"
        )
        chain = prompt | llm | StrOutputParser()
        try:
            return chain.invoke({"table": table_content[:3000]})
        except Exception as e:
            print(f"⚠️ 表格摘要生成失败: {e}")
            return "这是一个包含数据的学术表格。"

    def ingest_documents(self):
        """核心升级：多向量架构解析 PDF，分离图表与文本"""
        if not os.path.exists(self.raw_docs_path):
            os.makedirs(self.raw_docs_path)
            print(f"📁 已创建目录 {self.raw_docs_path}，请放入 PDF 文献！")
            return

        pdf_files = [f for f in os.listdir(self.raw_docs_path) if f.endswith('.pdf')]
        if not pdf_files:
            print("⚠️ 没有找到 PDF 文件，跳过建库。")
            return

        print(f"📚 发现 {len(pdf_files)} 篇文献，开始使用 Kimi 解析并执行多路结构化切分...")

        vector_docs = []  # 存入 FAISS 的【摘要/文本块】
        store_docs = []  # 存入底层 KV Store 的【完整原始表格/大文本块】
        bm25_docs = []  # 用于构建 BM25 的文档集

        for file in pdf_files:
            file_path = os.path.join(self.raw_docs_path, file)
            # 使用 Kimi 提取高精度 Markdown
            md_file_path = self.parser.parse_pdf(file_path)

            with open(md_file_path, "r", encoding="utf-8") as f:
                md_text = f.read()

            # 分离出表格和文本
            elements = self._extract_elements(md_text, file)

            # --- 处理表格 (多向量逻辑) ---
            if elements['tables']:
                print(f"📊 在 {file} 中发现 {len(elements['tables'])} 个表格，正在呼叫大模型生成高维语义摘要...")

            for tb in elements['tables']:
                doc_id = str(uuid.uuid4())
                # 1. 生成摘要存入 FAISS
                summary = self._summarize_table(tb["content"])
                summary_doc = Document(
                    page_content=summary,
                    metadata={self.id_key: doc_id, "source": tb["source"], "type": "table"}
                )
                vector_docs.append(summary_doc)
                bm25_docs.append(summary_doc)  # 摘要也参与关键词检索

                # 2. 将毫无损耗的原始表格存入底层 LocalFileStore
                store_docs.append((doc_id, tb["content"].encode('utf-8')))

            # --- 处理纯文本 ---
            for txt_doc in elements['texts']:
                doc_id = str(uuid.uuid4())
                # 文本块挂载相同的 UUID，方便后续统一通过 MultiVector 召回
                txt_doc.metadata[self.id_key] = doc_id
                txt_doc.metadata["type"] = "text"
                vector_docs.append(txt_doc)
                bm25_docs.append(txt_doc)
                # 同样存入底层
                store_docs.append((doc_id, txt_doc.page_content.encode('utf-8')))

        print("🧠 正在构建 FAISS 语义索引及本地 KV 存储引擎...")
        # 1. 构建 FAISS
        self.vector_store = FAISS.from_documents(vector_docs, self.embeddings)
        self.vector_store.save_local(self.vector_db_path)

        # 2. 将底层原始文档存入 KV Store
        self.byte_store.mset(store_docs)

        # 3. 组装 MultiVectorRetriever
        self.multi_retriever = MultiVectorRetriever(
            vectorstore=self.vector_store,
            byte_store=self.byte_store,
            id_key=self.id_key,
        )

        print("🔤 正在构建 BM25 关键词索引...")
        self.bm25_retriever = BM25Retriever.from_documents(bm25_docs)
        self.bm25_retriever.k = 5
        with open(self.bm25_path, 'wb') as f:
            pickle.dump(self.bm25_retriever, f)

        print("✅ 知识库多模态架构构建完成！")

    def _is_index_outdated(self) -> bool:
        if not os.path.exists(self.vector_db_path) or not os.path.exists(self.bm25_path) or not os.path.exists(
                self.kv_store_path):
            return True
        faiss_index_file = os.path.join(self.vector_db_path, "index.faiss")
        if not os.path.exists(faiss_index_file):
            return True
        index_mtime = os.path.getmtime(faiss_index_file)
        if os.path.exists(self.raw_docs_path):
            for file in os.listdir(self.raw_docs_path):
                if file.endswith('.pdf'):
                    pdf_path = os.path.join(self.raw_docs_path, file)
                    if os.path.getmtime(pdf_path) > index_mtime:
                        return True
        return False

    def load_or_build_index(self):
        if not self._is_index_outdated():
            print("🚀 加载已存在的多向量 FAISS、KV Store 和 BM25 索引...")
            self.vector_store = FAISS.load_local(
                self.vector_db_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            # 重新组装多向量检索器
            self.multi_retriever = MultiVectorRetriever(
                vectorstore=self.vector_store,
                byte_store=self.byte_store,
                id_key=self.id_key,
            )
            with open(self.bm25_path, 'rb') as f:
                self.bm25_retriever = pickle.load(f)
        else:
            print("⚠️ 索引缺失或已过期，触发重建逻辑...")
            self.ingest_documents()

    def retrieve(self, query: str, top_k: int = 4) -> List[Document]:
        """融合检索：先走语义和词频，再通过映射拿回原始文档（保留完美表格结构）"""
        if not self.multi_retriever or not self.bm25_retriever:
            self.load_or_build_index()

        if not self.multi_retriever or not self.bm25_retriever:
            return []

        # 注意这里：语义搜索使用 multi_retriever，这样拿到的是底层的完整表格，而非摘要！
        faiss_docs = self.multi_retriever.invoke(query)
        bm25_docs = self.bm25_retriever.invoke(query)

        # 将 BM25 拿到的摘要，也尝试去底层还原为原始表格
        mapped_bm25_docs = []
        for doc in bm25_docs:
            doc_id = doc.metadata.get(self.id_key)
            if doc_id:
                raw_bytes = self.byte_store.mget([doc_id])[0]
                if raw_bytes:
                    mapped_bm25_docs.append(Document(page_content=raw_bytes.decode('utf-8'), metadata=doc.metadata))
                else:
                    mapped_bm25_docs.append(doc)
            else:
                mapped_bm25_docs.append(doc)

        # 执行 RRF 融合打分
        c = 60
        fused_scores = {}
        doc_map = {}

        for rank, doc in enumerate(mapped_bm25_docs):
            content_hash = doc.page_content
            if content_hash not in doc_map:
                doc_map[content_hash] = doc
            fused_scores[content_hash] = fused_scores.get(content_hash, 0) + 1 / (rank + c)

        for rank, doc in enumerate(faiss_docs):
            content_hash = doc.page_content
            if content_hash not in doc_map:
                doc_map[content_hash] = doc
            fused_scores[content_hash] = fused_scores.get(content_hash, 0) + 1 / (rank + c)

        sorted_docs = sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
        return [doc_map[content] for content, score in sorted_docs[:top_k]]