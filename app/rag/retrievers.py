import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
import pickle
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever

# 引入基于 API 的解析器
from app.rag.pdf_parser import KimiAPIParser


class OmniRetriever:
    def __init__(self, raw_docs_path: str, vector_db_path: str):
        self.raw_docs_path = raw_docs_path
        self.vector_db_path = vector_db_path
        self.bm25_path = f"{vector_db_path}_bm25.pkl"

        # 初始化 MinerU API 解析器
        self.parser = KimiAPIParser(output_dir=f"{raw_docs_path}_parsed")

        print("⏳ 正在加载 Embedding 模型...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-zh-v1.5",
            model_kwargs={'device': 'cpu'}
        )
        self.vector_store = None
        self.bm25_retriever = None

    def ingest_documents(self):
        """升级版：使用 MinerU 解析 PDF 为 Markdown 并基于结构切分"""
        if not os.path.exists(self.raw_docs_path):
            os.makedirs(self.raw_docs_path)
            print(f"📁 已创建目录 {self.raw_docs_path}，请放入 PDF 文献！")
            return

        pdf_files = [f for f in os.listdir(self.raw_docs_path) if f.endswith('.pdf')]
        if not pdf_files:
            print("⚠️ 没有找到 PDF 文件，跳过建库。")
            return

        print(f"📚 发现 {len(pdf_files)} 篇文献，开始结构化解析...")
        docs = []

        # 定义 Markdown 切分规则（根据论文常见的标题层级）
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

        for file in pdf_files:
            file_path = os.path.join(self.raw_docs_path, file)

            # 1. 核心升级：使用 MinerU 提取 Markdown
            md_file_path = self.parser.parse_pdf(file_path)

            # 2. 读取生成的 Markdown 内容
            with open(md_file_path, "r", encoding="utf-8") as f:
                md_text = f.read()

            # 3. 按 Markdown 层级进行结构化切分
            md_splits = markdown_splitter.split_text(md_text)

            # 将来源文件名加入 Metadata，方便溯源
            for split in md_splits:
                split.metadata["source"] = file

            docs.extend(md_splits)

        print(f"✂️ 文献已按逻辑结构切分为 {len(docs)} 个 Chunk。")

        # 后续构建 FAISS 向量库和 BM25 索引的逻辑保持不变
        print("🧠 正在构建 FAISS 语义索引...")
        self.vector_store = FAISS.from_documents(docs, self.embeddings)
        self.vector_store.save_local(self.vector_db_path)

        print("🔤 正在构建 BM25 关键词索引...")
        self.bm25_retriever = BM25Retriever.from_documents(docs)
        self.bm25_retriever.k = 5

        with open(self.bm25_path, 'wb') as f:
            pickle.dump(self.bm25_retriever, f)

        print("✅ 知识库构建完成！")

    def _is_index_outdated(self) -> bool:
        """检测索引是否缺失，或者原始文献是否有更新"""
        if not os.path.exists(self.vector_db_path) or not os.path.exists(self.bm25_path):
            return True  # 索引完全不存在

        faiss_index_file = os.path.join(self.vector_db_path, "index.faiss")
        if not os.path.exists(faiss_index_file):
            return True

        # 获取当前索引的最后生成时间
        index_mtime = os.path.getmtime(faiss_index_file)

        # 检查 raw_docs_path 下是否有任何 PDF 文件的修改时间晚于索引生成时间
        if os.path.exists(self.raw_docs_path):
            for file in os.listdir(self.raw_docs_path):
                if file.endswith('.pdf'):
                    pdf_path = os.path.join(self.raw_docs_path, file)
                    if os.path.getmtime(pdf_path) > index_mtime:
                        return True  # 发现更新的 PDF，判定为索引已过期
        return False

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