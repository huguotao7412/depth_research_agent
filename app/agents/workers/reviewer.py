# app/agents/workers/reviewer.py
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from app.core.state import ResearchState


def reviewer_node(state: ResearchState) -> dict:
    llm = ChatOpenAI(model="deepseek-chat", temperature=0.3)
    instruction = state.get("current_instruction")
    task_desc = instruction.task_description if instruction else "审查当前的资料和草稿质量"

    collected_data = "\n".join([f"- {d['task']}: {d['extracted_info']}" for d in state.get("collected_data", [])])
    final_draft = state.get("final_draft", "暂无草稿")

    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个严苛的同行评审专家 (Reviewer)。"
                   "你的任务是审查系统当前收集的数据和撰写的草稿，指出逻辑漏洞、论据不足或表述不严谨的地方。\n"
                   "请给出建设性的修改意见，如果发现重要参考文献缺失，请明确指出需要补充检索的方向。"),
        MessagesPlaceholder(variable_name="messages"),
        ("user", "主管指令：{instruction}\n\n"
                 "【当前已收集数据】：\n{data}\n\n"
                 "【当前报告草稿】：\n{draft}\n\n"
                 "请输出你的审查意见。")
    ])

    chain = prompt | llm
    result_msg = chain.invoke({
        "messages": state["messages"],  # ✅ 补充这一行
        "instruction": task_desc,
        "data": collected_data if collected_data else "暂无",
        "draft": final_draft
    })

    # 获取已有列表副本，避免原地修改(append)影响历史状态树
    existing_comments = state.get("review_comments", [])

    return {
        "messages": [AIMessage(content=f"【审查意见】\n{result_msg.content}", name="Reviewer")],
        "review_comments": existing_comments + [result_msg.content]
    }