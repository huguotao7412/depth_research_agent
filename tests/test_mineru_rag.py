# tests/test_mineru_rag.py
import os
import sys
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

# 将项目根目录加入系统路径，确保能导入 app 模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入我们刚刚重构的 OmniRetriever (请确保 app/rag/retrievers.py 和 app/rag/pdf_parser.py 已经按之前的方案修改好)
from app.rag.retrievers import OmniRetriever


def main():
    # 1. 设置测试路径
    # 我们在 tests/data 下专门建一个测试用的目录
    test_docs_path = os.path.join(os.path.dirname(__file__), "data", "test_raw_docs")
    test_db_path = os.path.join(os.path.dirname(__file__), "data", "test_vector_db")

    # 确保文档目录存在
    os.makedirs(test_docs_path, exist_ok=True)

    print(f"👉 请确保你已经放了一篇 PDF 论文在以下目录：\n{test_docs_path}")
    print("等待你放入 PDF 文件...(如果已经放入，请按回车继续)")
    input()

    # 检查是否有 PDF
    if not any(f.endswith('.pdf') for f in os.listdir(test_docs_path)):
        print("❌ 目录里没有 PDF 文件，测试退出。")
        return

    # 2. 初始化重构后的检索器
    print("\n🚀 [1/3] 初始化 OmniRetriever...")
    retriever = OmniRetriever(
        raw_docs_path=test_docs_path,
        vector_db_path=test_db_path
    )

    # 3. 执行建库 (这里会触发 MinerU 解析和切分)
    print("\n🚀 [2/3] 开始解析 PDF 并构建多模态知识库...")
    # 强制重新建库以测试解析过程
    retriever.ingest_documents()

    # 4. 测试检索效果
    # 假设你的文献是关于毫米波雷达的，你可以修改下面这个 Query
    test_query = "毫米波雷达在心率监测中的主要挑战是什么？"

    print(f"\n🚀 [3/3] 测试检索效果，Query: '{test_query}'")
    retrieved_docs = retriever.retrieve(test_query, top_k=3)

    print("\n" + "=" * 50)
    print("✅ 检索结果展示：")
    print("=" * 50)

    if not retrieved_docs:
        print("未能检索到相关内容。")
    else:
        for i, doc in enumerate(retrieved_docs):
            print(f"\n--- 🏅 Top {i + 1} ---")
            # 重点观察 metadata 里是否包含了 Markdown 的 Header 结构
            print(f"📄 元数据 (Metadata): {doc.metadata}")
            print(f"📝 内容摘要 (前200字): \n{doc.page_content[:200]}...\n")


if __name__ == "__main__":
    main()