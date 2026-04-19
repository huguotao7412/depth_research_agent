# app/agents/workers/writer.py
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage
from app.core.state import ResearchState
from app.core.llm_factory import get_llm

# 🚨 引入隐式经验检索
from app.core.memory_store import search_experience


# 🚨 1. 直接将 compress_context 函数整个删除！不要用小模型压缩了！

def writer_node(state: ResearchState) -> dict:
    llm = get_llm(model_type="main", temperature=0.0)  # 保持温度为 0.0，杜绝发散
    instruction = state.get("current_instruction")
    task_desc = instruction.task_description if instruction and hasattr(instruction,
                                                                        'task_description') else "撰写或修改研究报告"

    # 🚨 获取当前工作区，并去 FAISS 库检索教训
    workspace_id = state.get("workspace_id", "default")
    past_lessons = search_experience(workspace_id, task_desc)

    plan_text = "\n".join([f"- {step}" for step in state.get("research_plan", [])])

    all_data = state.get("collected_data", [])
    recent_data = all_data[-5:] if len(all_data) > 5 else all_data

    # 1. 组装原始数据
    raw_data_list = []
    for d in recent_data:
        info = d.get('extracted_info', '')
        source = d.get('source', d.get('url', ''))
        if source:
            raw_data_list.append(f"- 【真实证据】: {info}\n  【唯一来源】: {source}")
        else:
            raw_data_list.append(f"- 【真实证据】: {info}")

    data_text = "\n\n".join(raw_data_list)

    # 2. 获取 Reviewer 的反馈意见（如果是被打回重写的）
    messages = state.get("messages", [])
    reviewer_feedback = "无"

    for m in reversed(messages):
        if getattr(m, 'name', '') == "Reviewer":
            reviewer_feedback = m.content
            break
        elif getattr(m, 'name', '') == "Writer":
            # 如果逆向先找到了自己(Writer)的历史，说明这一轮是全新的，没有经过 Reviewer 打回
            break

    # 3. 动态构建系统提示词
    system_prompt = (
        "你是一个严谨的学术报告撰写者 (Writer)。\n"
        "请根据收集到的【核心事实数据】，将其转化为连贯、专业的学术研究报告初稿。\n"
        "你的核心能力是将散乱的数据整合成逻辑严密、专业客观的文本。\n\n"
        "🎯 【排版指导】：\n"
        "如果是撰写『国内外研究现状』或『文献综述』，请**弱化各级标题，采用自然流畅的段落过渡**，大标题数量应少于3个。\n\n"
        "⚠️ 【反幻觉与引用铁律 - 如果违反你将被判定为失败】：\n"
        "1. 绝不能凭空捏造！每一句陈述、每一个数据，都【必须】严格基于我提供给你的【带来源的素材库】。\n"
        "2. 如果【带来源的素材库】为空，或者里面的内容不足以支撑写作，你必须直接在正文回复：『抱歉，由于未能检索到有效的学术数据，无法完成本节撰写』。绝对禁止基于你的预训练知识编造内容！\n"
        "3. 引用必须挂靠在句子末尾。对于本地文献使用 `(来源: xxx.pdf)`；对于网络搜索，必须提取 URL，使用 Markdown 超链接格式 `[参考网页](完整的URL)`。\n"
        "4. 不要生成任何“由于技术限制无法提供链接”之类的借口，有链接就写，没检索到就直接报错。"
    )

    # 🚨 动态注入心智：贴上避坑指南
    if past_lessons:
        system_prompt += (
            f"\n\n⚠️ 【历史经验教训 / 避坑指南】:\n"
            f"{past_lessons}\n"
            "(请务必在撰写本次报告时规避上述提到的历史错误，满足用户的深层要求。)"
        )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        ("user", "主管指令：{instruction}\n\n"
                 "【研究大纲】：\n{plan}\n\n"
                 "【带来源的素材库 (你的唯一信息源)】：\n{data}\n\n"
                 "【Reviewer的修改建议 (若有)】：\n{feedback}")
    ])

    try:
        result = (prompt | llm).invoke({
            "messages": messages,
            "instruction": task_desc,
            "plan": plan_text,
            "data": data_text,
            "feedback": reviewer_feedback
        })

        response_msg = AIMessage(content=f"【Writer 初稿已完成】\n\n{result.content}", name="Writer")
        return {
            "messages": [response_msg],
            "final_draft": result.content
        }
    except Exception as e:
        print(f"Writer 节点执行失败: {e}")
        return {"messages": [AIMessage(content=f"【Writer 报错】撰写失败: {str(e)}", name="Writer")]}