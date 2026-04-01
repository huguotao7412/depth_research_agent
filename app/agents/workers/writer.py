# app/agents/workers/writer.py
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage
from app.core.state import ResearchState
from app.core.llm_factory import get_llm


# 🚀 优化点 1：新增一个轻量级的上下文压缩函数
def compress_context(raw_data_list: list, plan_text: str) -> str:
    """使用轻量模型对庞大的检索素材进行去重和核心信息提炼，防止主模型 Context 爆炸"""
    if not raw_data_list:
        return "暂无素材"

    print("   [Writer 预处理] 正在对海量检索数据进行压缩和去重...")

    # 使用轻量级模型来做信息压缩，降低成本
    cheap_llm = get_llm(model_type="fast", temperature=0.2)

    raw_text = "\n\n".join(raw_data_list)

    compress_prompt = ChatPromptTemplate.from_template(
        "你是一个学术数据整理助手。以下是 Researcher 收集到的大量原始数据。\n"
        "请根据【研究大纲】，对这些数据进行总结、去重和提炼。\n\n"
        "⚠️ 【绝对不可妥协的原则】：\n"
        "必须保留所有重要的事实、数据指标，并且【绝对不能丢弃任何 [来源] 信息】！\n"
        "如果在提炼某段内容，必须把原有的来源标记（如URL或文件名）附在提炼后的内容旁。\n\n"
        "【研究大纲】：\n{plan}\n\n"
        "【原始数据】：\n{raw_data}\n\n"
        "请输出高密度、保留引用的浓缩版素材库："
    )

    chain = compress_prompt | cheap_llm
    result = chain.invoke({"plan": plan_text, "raw_data": raw_text})
    return result.content


def writer_node(state: ResearchState) -> dict:
    # 主力模型负责最终的深度行文
    llm = get_llm(model_type="main", temperature=0.0)
    instruction = state.get("current_instruction")
    task_desc = instruction.task_description if instruction and hasattr(instruction,
                                                                        'task_description') else "撰写或修改研究报告"

    plan_text = "\n".join([f"- {step}" for step in state.get("research_plan", [])])

    # 1. 组装原始数据
    raw_data_list = []
    for d in state.get("collected_data", []):
        info = d.get('extracted_info', '')
        source = d.get('source', d.get('url', ''))
        if source:
            raw_data_list.append(f"- 【内容】: {info}\n  【来源】: {source}")
        else:
            raw_data_list.append(f"- 【内容】: {info}")

    # 🚀 优化点 2：触发上下文压缩机制，解决 Lost in the middle 隐患
    # 如果条目太多（比如超过3条或文本过长），则进行压缩
    if len(raw_data_list) > 3 or len(str(raw_data_list)) > 4000:
        compressed_data = compress_context(raw_data_list, plan_text if plan_text else "无")
    else:
        compressed_data = "\n\n".join(raw_data_list)

    reviews = "\n".join(state.get("review_comments", []))
    current_draft = state.get("final_draft", "")

    # 3. 核心行文 System Prompt 保持严谨规范
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个资深的学术撰稿人 (Writer)。"
                   "你的任务是将散乱的数据、规划和审查意见整合成逻辑严密、专业客观的文本。\n\n"
                   "🎯 【排版与行文风格指导】：\n"
                   "请根据主管的具体指令动态调整你的写作格式：\n"
                   "- 如果任务是撰写『研究报告』或『深度分析』，请使用清晰的层级标题（H2, H3）来组织结构。\n"
                   "- 如果任务是撰写『国内外研究现状』、『文献综述』或『背景介绍』，请**弱化各级标题，采用自然流畅的段落过渡**，像叙述学术发展史一样将各个研究成果串联起来，仅在必要时使用少量的大模块标题,且大标题数量应少于3个。\n\n"
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

    print("   [Writer] 正在基于素材与审查意见奋笔疾书...")
    result_msg = chain.invoke({
        "messages": state["messages"],
        "instruction": task_desc,
        "plan": plan_text if plan_text else "暂无大纲",
        "data": compressed_data,
        "reviews": reviews if reviews else "暂无修改意见",
        "draft": current_draft if current_draft else "从零开始撰写"
    })

    return {
        "messages": [AIMessage(content=f"【撰写完成/更新】\n已生成带有规范引用的最新版本草稿。", name="Writer")],
        "final_draft": result_msg.content
    }