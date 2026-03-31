# app/agents/workers/writer.py
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from app.core.state import ResearchState


def writer_node(state: ResearchState) -> dict:
    llm = ChatOpenAI(model="deepseek-chat", temperature=0.4)  # 温度稍高一点，利于连贯写作
    instruction = state.get("current_instruction")
    task_desc = instruction.task_description if instruction else "撰写或修改研究报告"

    # 聚合系统状态，为 Writer 提供全局视野
    plan_text = "\n".join([f"- {step}" for step in state.get("research_plan", [])])
    collected_data = "\n".join([f"- {d['extracted_info']}" for d in state.get("collected_data", [])])
    reviews = "\n".join(state.get("review_comments", []))
    current_draft = state.get("final_draft", "")

    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个资深的学术撰稿人 (Writer)。"
                   "你的任务是将散乱的数据、规划和审查意见整合成逻辑严密、格式规范的学术报告。\n"
                   "要求语言专业客观，采用学术论文的结构风格。"),
        MessagesPlaceholder(variable_name="messages"),
        ("user", "主管指令：{instruction}\n\n"
                 "【研究大纲】：\n{plan}\n\n"
                 "【素材库】：\n{data}\n\n"
                 "【Reviewer的修改意见】：\n{reviews}\n\n"
                 "【历史草稿（如有）】：\n{draft}\n\n"
                 "请撰写或更新最终报告内容。")
    ])

    chain = prompt | llm
    result_msg = chain.invoke({
        "messages": state["messages"],  # ✅ 必须加上这一行，把历史消息传给占位符
        "instruction": task_desc,
        "plan": plan_text if plan_text else "暂无",
        "data": collected_data if collected_data else "暂无素材",
        "reviews": reviews if reviews else "暂无修改意见",
        "draft": current_draft if current_draft else "从零开始撰写"
    })

    return {
        "messages": [AIMessage(content=f"【撰写完成/更新】\n已生成最新版本草稿，见工作区。", name="Writer")],
        "final_draft": result_msg.content
    }