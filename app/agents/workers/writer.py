# app/agents/workers/writer.py

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage
from app.core.state import ResearchState
from app.core.llm_factory import get_llm

# 🚨 1. 直接将 compress_context 函数整个删除！不要用小模型压缩了！

def writer_node(state: ResearchState) -> dict:
    llm = get_llm(model_type="main", temperature=0.0) # 保持温度为 0.0，杜绝发散
    instruction = state.get("current_instruction")
    task_desc = instruction.task_description if instruction and hasattr(instruction, 'task_description') else "撰写或修改研究报告"

    plan_text = "\n".join([f"- {step}" for step in state.get("research_plan", [])])

    # 1. 组装原始数据
    raw_data_list = []
    for d in state.get("collected_data", []):
        info = d.get('extracted_info', '')
        source = d.get('source', d.get('url', ''))
        if source:
            raw_data_list.append(f"- 【真实证据】: {info}\n  【唯一来源】: {source}")
        else:
            raw_data_list.append(f"- 【真实证据】: {info}")

    # 🚨 2. 直接使用原生拼接数据，跳过所有二次压缩
    compressed_data = "\n\n".join(raw_data_list)

    reviews = "\n".join(state.get("review_comments", []))
    current_draft = state.get("final_draft", "")

    # 🚨 3. 增强 System Prompt 的“杀伤力”，禁止大模型自我发挥
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个资深的学术撰稿人 (Writer)。"
                   "你的任务是将散乱的数据整合成逻辑严密、专业客观的文本。\n\n"
                   "🎯 【排版指导】：\n"
                   "如果是撰写『国内外研究现状』或『文献综述』，请**弱化各级标题，采用自然流畅的段落过渡**，大标题数量应少于3个。\n\n"
                   "⚠️ 【反幻觉与引用铁律 - 如果违反你将被判定为失败】：\n"
                   "1. 绝不能凭空捏造！每一句陈述、每一个数据，都【必须】严格基于我提供给你的【带来源的素材库】。\n"
                   "2. 如果【带来源的素材库】为空，或者里面的内容不足以支撑写作，你必须直接在正文回复：『抱歉，由于未能检索到有效的学术数据，无法完成本节撰写』。绝对禁止基于你的预训练知识编造内容！\n"
                   "3. 引用必须挂靠在句子末尾。对于本地文献使用 `(来源: xxx.pdf)`；对于网络搜索，必须提取 URL，使用 Markdown 超链接格式 `[参考网页](完整的URL)`。\n"
                   "4. 不要生成任何“由于技术限制无法提供链接”之类的借口，有链接就写，没检索到就直接报错。"),
        MessagesPlaceholder(variable_name="messages"),
        ("user", "主管指令：{instruction}\n\n"
                 "【研究大纲】：\n{plan}\n\n"
                 "【带来源的素材库 (你的唯一信息源)】：\n{data}\n\n"
                 "【Reviewer的修改意见】：\n{reviews}\n\n"
                 "【历史草稿（如有）】：\n{draft}\n\n"
                 "请撰写最终报告。")
    ])

    chain = prompt | llm

    print("   [Writer] 正在基于真实检索素材奋笔疾书...")
    result_msg = chain.invoke({
        "messages": state["messages"],
        "instruction": task_desc,
        "plan": plan_text if plan_text else "暂无大纲",
        "data": compressed_data if compressed_data else "【警告：当前素材库为空，请拒绝编造并要求退回检索】",
        "reviews": reviews if reviews else "暂无修改意见",
        "draft": current_draft if current_draft else "从零开始撰写"
    })

    return {
        "messages": [AIMessage(content=f"【撰写完成/更新】\n已生成带有规范引用的最新版本草稿。", name="Writer")],
        "final_draft": result_msg.content
    }