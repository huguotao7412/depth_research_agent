# app/agents/workers/daily_qa.py
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage
from app.core.state import ResearchState
from app.core.llm_factory import get_llm


def daily_qa_node(state: ResearchState) -> dict:
    print("\n⚡ [DailyQA] 触发快系统，正在使用低延迟模型极速响应...")
    session_summary = state.get("session_summary", "")

    # 调用响应速度极快的 fast 模型 (低 Temperature 保证回答的客观准确性)
    llm = get_llm(model_type="main", temperature=0.3)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个高效的学术概念解答助手 (DailyQA)。"
                   "你的任务是针对用户提出的基础概念、常识或技术名词，直接给出清晰、易懂的解答。"
                   "你不需要进行长篇大论，也不需要捏造文献引用，力求精准和极速即可。"),
        MessagesPlaceholder(variable_name="messages")
    ])
    if session_summary:
        prompt += (
            "\n\n🧠 【前置对话情境摘要】:\n"
            f"{session_summary}\n"
            "(请在理解用户意图和决定下一步动作时，务必参考上述历史背景，不要重复提问已知信息)\n"
        )

    chain = prompt | llm

    try:
        result_msg = chain.invoke({"messages": state["messages"]})
        reply_content = f"{result_msg.content}"
    except Exception as e:
        print(f"⚠️ [DailyQA] 执行失败: {str(e)}")
        reply_content = f"抱歉，快问快答模块响应异常: {str(e)}"

    # 同时返回 messages 和 final_draft，这样前端 UI 就能直接渲染结果
    return {
        "messages": [AIMessage(content=f"【快问快答】\n{reply_content}", name="DailyQA")],
        "final_draft": reply_content
    }