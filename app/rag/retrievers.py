import os
import pickle
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever


class OmniRetriever:
    def __init__(self, raw_docs_path: str, vector_db_path: str):
        self.raw_docs_path = raw_docs_path
        self.vector_db_path = vector_db_path
        # 指定 BM25 的本地缓存路径
        self.bm25_path = f"{vector_db_path}_bm25.pkl"

        # 1. 初始化本地 Embedding 模型
        print("⏳ 正在加载 Embedding 模型...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-zh-v1.5",
            model_kwargs={'device': 'cpu'}
        )

        self.vector_store = None
        self.bm25_retriever = None

    def ingest_documents(self):
        """加载本地 PDF 并构建索引"""
        if not os.path.exists(self.raw_docs_path):
            os.makedirs(self.raw_docs_path)
            print(f"📁 已创建目录 {self.raw_docs_path}，请放入 PDF 文献！")
            return

        pdf_files = [f for f in os.listdir(self.raw_docs_path) if f.endswith('.pdf')]
        if not pdf_files:
            print("⚠️ 没有找到 PDF 文件，跳过建库。")
            return

        print(f"📚 发现 {len(pdf_files)} 篇文献，开始解析...")
        docs = []
        for file in pdf_files:
            file_path = os.path.join(self.raw_docs_path, file)
            loader = PyMuPDFLoader(file_path)
            docs.extend(loader.load())

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", "。", "！", "？", " ", ""]
        )
        splits = text_splitter.split_documents(docs)
        print(f"✂️ 文献已切分为 {len(splits)} 个 Chunk。")

        # 构建 FAISS 向量库 (语义检索)
        print("🧠 正在构建 FAISS 语义索引...")
        self.vector_store = FAISS.from_documents(splits, self.embeddings)
        self.vector_store.save_local(self.vector_db_path)

        # 构建 BM25 索引 (关键词检索)
        print("🔤 正在构建 BM25 关键词索引...")
        self.bm25_retriever = BM25Retriever.from_documents(splits)
        # BM25 取前 5 个最相关的备用
        self.bm25_retriever.k = 5

        # 将 BM25 检索器序列化保存到本地，实现双路缓存
        with open(self.bm25_path, 'wb') as f:
            pickle.dump(self.bm25_retriever, f)

        print("✅ 知识库构建完成！")

    def load_or_build_index(self):
        """如果本地有缓存就加载，没有就重新构建"""
        if os.path.exists(self.vector_db_path) and os.path.exists(self.bm25_path):
            print("🚀 加载已存在的 FAISS 和 BM25 索引...")
            self.vector_store = FAISS.load_local(
                self.vector_db_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            # 加载本地缓存的 BM25，不再重新读取 PDF
            with open(self.bm25_path, 'rb') as f:
                self.bm25_retriever = pickle.load(f)
        else:
            print("⚠️ 索引不完整，正在重新构建...")
            self.ingest_documents()

    def retrieve(self, query: str, top_k: int = 4) -> List[Document]:
        """对外暴露的统一检索接口：手动实现 RRF 多路召回融合"""
        if not self.vector_store or not self.bm25_retriever:
            self.load_or_build_index()

        if not self.vector_store or not self.bm25_retriever:
            return []

        # 1. 分别执行两路查询
        faiss_retriever = self.vector_store.as_retriever(search_kwargs={"k": 5})
        bm25_docs = self.bm25_retriever.invoke(query)
        faiss_docs = faiss_retriever.invoke(query)

        # 2. 核心算法：RRF (Reciprocal Rank Fusion)
        c = 60
        fused_scores = {}
        doc_map = {}

        for rank, doc in enumerate(bm25_docs):
            content_hash = doc.page_content
            if content_hash not in doc_map:
                doc_map[content_hash] = doc
            fused_scores[content_hash] = fused_scores.get(content_hash, 0) + 1 / (rank + c)

        for rank, doc in enumerate(faiss_docs):
            content_hash = doc.page_content
            if content_hash not in doc_map:
                doc_map[content_hash] = doc
            fused_scores[content_hash] = fused_scores.get(content_hash, 0) + 1 / (rank + c)

        # 3. 按融合总得分降序排列
        sorted_docs = sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)

        # 4. 返回最终合并后的 Top-K 结果
        return [doc_map[content] for content, score in sorted_docs[:top_k]]