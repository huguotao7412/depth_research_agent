import os
import sys
from dotenv import load_dotenv
load_dotenv()

# 将项目根目录加入 sys.path，确保能正确导入 app 模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag.retrievers import OmniRetriever


def test_hybrid_search():
    # 1. 加载环境变量


    # 2. 路径配置
    # 注意这里要与你在 nodes.py 里 mock 的路径逻辑对齐，或者使用相对项目根目录的路径
    raw_docs_path = os.path.join("data", "raw_docs")
    vector_db_path = os.path.join("data", "vector_db", "faiss_index")

    print("🚀 初始化 OmniRetriever (双引擎多路召回)...")
    retriever = OmniRetriever(raw_docs_path=raw_docs_path, vector_db_path=vector_db_path)

    # 3. 触发文献入库或加载现有索引
    retriever.load_or_build_index()

    # 4. 执行测试提问
    query = "基于毫米波雷达提取脉搏波传导速度(PWV)进行连续血压预测时，主要的信号处理难点与误差来源是什么？"
    print(f"\n🔍 测试检索问题: {query}")
    print("-" * 50)

    # 5. 调用 invoke 执行混合检索
    docs = retriever.retrieve(query)

    if not docs:
        print("⚠️ 未检索到任何文档，请确保 data/raw_docs/ 目录下有 PDF 文件！")
        return

    print(f"✅ 成功召回 {len(docs)} 个高相关性片段：\n")
    for i, doc in enumerate(docs):
        # 打印来源和部分内容
        source = doc.metadata.get("source", "未知来源")
        file_name = os.path.basename(source)
        # 把换行符去掉，方便在终端干净地打印
        clean_content = doc.page_content.replace('\n', ' ')

        print(f"[{i + 1}] 来源: {file_name}")
        print(f"    内容: {clean_content[:150]}...\n")


if __name__ == "__main__":
    test_hybrid_search()