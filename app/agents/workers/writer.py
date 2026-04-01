# app/agents/workers/writer.py
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from app.core.state import ResearchState


def writer_node(state: ResearchState) -> dict:
    llm = ChatOpenAI(model="deepseek-chat", temperature=0.4)
    instruction = state.get("current_instruction")
    task_desc = instruction.task_description if instruction else "撰写或修改研究报告"

    # 1. 聚合系统状态，为 Writer 提供全局视野
    plan_text = "\n".join([f"- {step}" for step in state.get("research_plan", [])])

    # 2. 核心修改：在拼接收集到的数据时，尽最大可能保留和展示“来源（Source/URL）”
    data_list = []
    for d in state.get("collected_data", []):
        info = d.get('extracted_info', '')
        # 兼容不同的键名，有些可能叫 source，有些可能叫 url
        source = d.get('source', d.get('url', ''))

        if source:
            data_list.append(f"- 【内容】: {info}\n  【来源】: {source}")
        else:
            data_list.append(f"- 【内容】: {info}")

    collected_data = "\n".join(data_list)
    reviews = "\n".join(state.get("review_comments", []))
    current_draft = state.get("final_draft", "")

    # 3. 强化 System Prompt：引入严格的 Citation（引用）规范
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个资深的学术撰稿人 (Writer)。"
                   "你的任务是将散乱的数据、规划和审查意见整合成逻辑严密、专业客观的文本。\n\n"
                   "🎯 【排版与行文风格指导】：\n"
                   "请根据主管的具体指令动态调整你的写作格式：\n"
                   "- 如果任务是撰写『研究报告』或『深度分析』，请使用清晰的层级标题（H2, H3）来组织结构。\n"
                   "- 如果任务是撰写『国内外研究现状』、『文献综述』或『背景介绍』，请**弱化各级标题，采用自然流畅的段落过渡**，像叙述学术发展史一样将各个研究成果串联起来，仅在必要时使用少量的大模块标题。\n\n"
                   "⚠️ 【引用与来源规范 - 必须严格遵守】：\n"
                   "1. 绝不能凭空捏造，每一项关键结论、数据、引用都【必须】在对应的句子或段落末尾标明出处。\n"
                   "2. 请根据【素材库】中提供的【来源】信息进行精准标注。\n"
                   "3. 对于本地 PDF/文献库文档：请在句末使用格式 `(来源: xxx.pdf)`。\n"
                   "4. 对于网络搜索结果（包含 http/https 链接）：请提取素材中的 URL，并**务必使用 Markdown 的超链接语法**将其隐藏！\n"
                   "   - 正确示例：`数据表明全球变暖加剧 ([参考网页](https://example.com))`\n"
                   "   - 错误示例：`数据表明全球变暖加剧 (来源网页: https://example.com)`\n"
                   "   **绝不能将纯文本的长 URL 直接暴露在正文中！**\n"
                   "5. 如果素材库中某条信息没有提供来源，尽量结合上下文合理表述，但不要自己伪造链接。"),
        MessagesPlaceholder(variable_name="messages"),
        ("user", "主管指令：{instruction}\n\n"
                 "【研究大纲】：\n{plan}\n\n"
                 "【带来源的素材库】：\n{data}\n\n"
                 "【Reviewer的修改意见】：\n{reviews}\n\n"
                 "【历史草稿（如有）】：\n{draft}\n\n"
                 "请撰写或更新最终报告内容。请务必使用美观的 Markdown 语法并严格按照规范标注出处！")
    ])

    chain = prompt | llm
    result_msg = chain.invoke({
        "messages": state["messages"],
        "instruction": task_desc,
        "plan": plan_text if plan_text else "暂无大纲",
        "data": collected_data if collected_data else "暂无素材",
        "reviews": reviews if reviews else "暂无修改意见",
        "draft": current_draft if current_draft else "从零开始撰写"
    })

    return {
        "messages": [AIMessage(content=f"【撰写完成/更新】\n已生成带有规范引用的最新版本草稿，见工作区。", name="Writer")],
        "final_draft": result_msg.content
    }