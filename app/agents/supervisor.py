# app/agents/supervisor.py
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from protocols.a2a.schemas import SupervisorDecision
from app.core.state import ResearchState


def create_supervisor_node(llm: ChatOpenAI):
    system_prompt = (
        "你是一个顶尖学术研究团队的主管 (Supervisor)。"
        "你的目标是通过协调以下团队成员来完成用户的最终研究任务：\n"
        "1. Planner: 负责拆解复杂的学术问题，制定研究大纲。\n"
        "2. Researcher: 负责检索外网或本地向量库，收集学术资料和数据。\n"
        "3. Reviewer: 负责审查 Researcher 收集的资料以及 Writer 写的草稿，检查逻辑闭环和事实准确性。\n"
        "4. Writer: 负责根据收集的资料和审查意见，撰写最终的学术报告。\n\n"
        "请根据当前的任务进度，决定下一步该由谁来工作。如果认为任务已圆满完成，请选择 'FINISH'。"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        ("system", "请基于以上进度，做出下一步的调度决策。")
    ])

    # 强制 LLM 输出符合 A2A 协议的结构化决策
    supervisor_chain = prompt | llm.with_structured_output(
        SupervisorDecision,
        method="function_calling"
    )

    def supervisor_node(state: ResearchState) -> dict:
        decision: SupervisorDecision = supervisor_chain.invoke(state)
        # 将决策转化为状态更新
        return {
            "next": decision.next_agent,
            "current_instruction": decision.instruction
        }

    return supervisor_node