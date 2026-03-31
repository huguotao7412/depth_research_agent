# app/agents/workers/reviewer.py
import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from app.core.state import ResearchState


def reviewer_node(state: ResearchState) -> dict:
    llm = ChatOpenAI(api_key=os.getenv("ZHIPU_API_KEY"),
                     base_url="https://open.bigmodel.cn/api/paas/v4/",
                     model="glm-4-flash",
                     temperature=0.2
                     )
    instruction = state.get("current_instruction")
    task_desc = instruction.task_description if instruction else "审查当前的资料和草稿质量"

    collected_data = "\n".join([f"- {d['task']}: {d['extracted_info']}" for d in state.get("collected_data", [])])
    final_draft = state.get("final_draft", "暂无草稿")

    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个严苛但讲理的同行评审专家 (Reviewer)。"
                   "你的任务是审查系统当前撰写的草稿，指出逻辑漏洞、论据不足或表述不严谨的地方。\n\n"
                   "⚠️ 【关键动作指令 - 必须遵守】：\n"
                   "1. 拦截空草稿：如果当前报告草稿提示为“暂无草稿”或内容极少，请直接输出：“当前尚未生成草稿，请退回给 Writer 执行撰写任务”。【绝对不能】输出 APPROVED 或通过！\n"
                   "2. 提出修改：如果草稿存在严重问题，请给出明确的修改建议。\n"
                   "3. 验收通过：如果草稿质量已经达标，或者经过修改后已经没有明显的逻辑硬伤，你【必须】在回复的最开头明确输出 'APPROVED'。"),
        MessagesPlaceholder(variable_name="messages"),
        ("user", "主管指令：{instruction}\n\n"
                 "【当前已收集数据】：\n{data}\n\n"
                 "【当前报告草稿】：\n{draft}\n\n"
                 "请输出你的审查意见。如果草稿不存在，请打回；如果认为达标，请务必在开头包含 'APPROVED'。")
    ])

    chain = prompt | llm
    result_msg = chain.invoke({
        "messages": state["messages"],
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