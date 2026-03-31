# app/agents/workers/researcher.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from app.core.state import ResearchState
from app.rag.retrievers import OmniRetriever  # ✅ 修正导入类名


def researcher_node(state: ResearchState) -> dict:
    llm = ChatOpenAI(
        model="deepseek-chat",
        temperature=0,
        timeout=60,  # 如果60秒没响应直接打断
        max_retries=2  # 失败自动重试2次
    )
    instruction = state.get("current_instruction")
    task_desc = instruction.task_description if instruction else "检索相关文献并提取关键数据"

    # 1. 动态获取 API 传进来的知识库路径
    raw_path = state.get("raw_docs_path", "data/raw_docs")
    db_path = state.get("vector_db_path", "data/vector_db/faiss_index")

    # 2. 正确实例化重构后的 OmniRetriever
    retriever = OmniRetriever(raw_docs_path=raw_path, vector_db_path=db_path)

    # 3. 使用正确的方法 retrieve 进行召回
    docs = retriever.retrieve(task_desc)
    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个高效的学术研究员 (Researcher)。"
                   "你负责从提供的原始资料中提取高价值的学术信息，过滤掉无关噪音。\n"
                   "当前任务：{instruction}\n\n"
                   "参考资料来源：\n{context}"),
        ("user", "请根据上述资料和任务指令，整理出有用的数据卡片或文献摘要。")
    ])

    chain = prompt | llm
    result_msg = chain.invoke({
        "instruction": task_desc,
        "context": context
    })

    new_data = {
        "task": task_desc,
        "extracted_info": result_msg.content
    }

    # ✅ 4. 修复：使用纯函数式合并，避免 list.append() 直接修改引用产生的不可预知覆盖
    existing_data = state.get("collected_data", [])

    return {
        "messages": [AIMessage(content=f"【资料收集完毕】\n{result_msg.content}", name="Researcher")],
        "collected_data": existing_data + [new_data]  # ✅ 安全赋值
    }