# app/agents/workers/memory_manager.py
from langchain_core.messages import HumanMessage, RemoveMessage
from app.core.state import ResearchState
from app.core.llm_factory import get_llm


async def memory_manager_node(state: ResearchState) -> dict:
    messages = state.get("messages", [])
    summary = state.get("session_summary", "")

    # 滑动窗口机制：保留最近的 6 条消息 (约 3 轮对话)，超过 12 条才触发压缩防爆
    if len(messages) > 12:
        print(f"\n🧠 [Memory Engine] 历史对话达到 {len(messages)} 条，触发 FAST_LLM 异步摘要...")
        messages_to_summarize = messages[:-6]  # 取出需要抛弃的老旧消息

        # 调取极速/廉价模型 (GLM-4-Flash)
        fast_llm = get_llm(model_type="fast", temperature=0.1)

        prompt = (
            "你是一个学术 Agent 的记忆压缩模块。请将以下早期的对话历史压缩成一段精炼的情境摘要（Context Summary）。\n"
            "【要求】保留用户的核心研究意图、领域偏好设定、以及已经得出的关键结论。直接输出摘要，不要废话。\n\n"
        )
        if summary:
            prompt += f"【原有的长期摘要】:\n{summary}\n\n"

        prompt += "【需要压缩的近期对话】:\n"
        for m in messages_to_summarize:
            role = "User" if isinstance(m, HumanMessage) else "AI"
            # 防御性截断，防止单条消息内含大篇幅报告
            content = str(m.content)[:400] + "..." if len(str(m.content)) > 400 else str(m.content)
            prompt += f"{role}: {content}\n"

        try:
            new_summary = await fast_llm.ainvoke([HumanMessage(content=prompt)])
            print("🧠 [Memory Engine] 摘要生成完毕，正在清理冗余 Context Window。")

            # 返回新的摘要，并通过内置的 RemoveMessage 指令删除老消息，彻底释放 Token
            # 注意：只有带有 id 的 message 才能被 RemoveMessage 成功删除
            return {
                "session_summary": new_summary.content,
                "messages": [RemoveMessage(id=m.id) for m in messages_to_summarize if getattr(m, "id", None)]
            }
        except Exception as e:
            print(f"⚠️ [Memory Engine] 摘要生成失败，保留原消息: {e}")
            return {}

    return {}  # 未达阈值，无事发生