# app/agents/workers/memory_manager.py
from langchain_core.messages import HumanMessage, RemoveMessage, AIMessage
from pydantic import BaseModel, Field
from app.core.state import ResearchState
from app.core.llm_factory import get_llm
from app.core.memory_store import update_profile, add_experience

class MemoryExtraction(BaseModel):
    new_preferences: dict = Field(default_factory=dict, description="提取的结构化偏好(如核心算法、输出格式要求等)，以字典形式返回")
    lessons_learned: list[str] = Field(default_factory=list, description="提取的用户明确指出的错误、批评、教训或修改意见。若无则为空列表")


async def memory_manager_node(state: ResearchState) -> dict:
    messages = state.get("messages", [])
    summary = state.get("session_summary", "")
    workspace_id = state.get("workspace_id", "default")

    # ==========================================
    # 🌟 长期记忆心智提炼 (Long-term Extraction)
    # ==========================================
    print("\n🕵️ [Memory Engine] 正在后台静默提炼长期偏好与经验教训...")
    try:
        extractor_llm = get_llm(model_type="main", temperature=0.1)

        # 只提取最近几轮对话，避免过度发散
        recent_context = "\n".join(
            [f"{'User' if isinstance(m, HumanMessage) else 'AI'}: {str(m.content)[:300]}" for m in messages[-4:]])

        extract_prompt = (
            "你是一个学术 Agent 的记忆提取中枢。请分析最近的对话，提取以下信息：\n"
            "1. 用户是否有明确的研究偏好、关注的算法或格式要求？(提取入 new_preferences)\n"
            "2. 用户是否有对之前输出的批评、纠正或要求避坑的地方？(提取入 lessons_learned)\n"
            f"近期对话记录：\n{recent_context}"
        )

        structured_llm = extractor_llm.with_structured_output(MemoryExtraction)
        extraction: MemoryExtraction = await structured_llm.ainvoke(extract_prompt)

        if extraction.new_preferences:
            update_profile(workspace_id, extraction.new_preferences)
            print(f"   [+] 成功提取偏好: {list(extraction.new_preferences.keys())}")
        if extraction.lessons_learned:
            add_experience(workspace_id, extraction.lessons_learned)
            print(f"   [+] 成功存入隐式经验: {len(extraction.lessons_learned)} 条")

    except Exception as e:
        print(f"   [⚠️] 长期记忆提炼跳过 (模型输出不规范或无新信息): {e}")

    # ==========================================
    # 🧹 短期记忆防爆与压缩 (Short-term Session)
    # (保留你原本写好的防爆逻辑)
    # ==========================================
    # 滑动窗口机制：保留最近的 6 条消息 (约 3 轮对话)，超过 12 条才触发压缩防爆
    if len(messages) > 12:
        print(f"\n🧠 [Memory Engine] 历史对话达到 {len(messages)} 条，触发 FAST_LLM 异步摘要...")
        messages_to_summarize = messages[:-6]  # 取出需要抛弃的老旧消息

        # 调取极速/廉价模型 (GLM-4-Flash)
        fast_llm = get_llm(model_type="main", temperature=0.1)

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