# app/agents/supervisor.py
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from protocols.a2a.schemas import SupervisorDecision
from app.core.state import ResearchState


def create_supervisor_node(llm: ChatOpenAI):
    system_prompt = (
        "你是一个顶尖学术研究团队的主管 (Supervisor)。"
        "你的目标是通过协调以下团队成员来完成用户的最终研究任务：\n"
        "1. Planner: 负责拆解复杂的学术问题，制定研究大纲。通常是任务的第一步。\n"
        "2. Researcher: 负责检索资料和数据。在 Planner 之后执行。\n"
        "3. Reviewer: 负责审查逻辑和事实准确性。\n"
        "4. Writer: 负责撰写最终的学术报告。\n\n"
        "⚠️ 【强制防死循环纪律 - 必须严格遵守】：\n"
        "1. 单向流转原则：不要让同一个 Agent 连续执行相同的任务！如果 Planner 已生成计划，下一步请指派 Researcher。\n"
        "2. 打断无限审查：仔细阅读最近的聊天记录，如果 Reviewer 的最新反馈中包含 '通过'、'APPROVED'、'建议通过' 或认为没有大问题，你【必须】直接选择 'FINISH' 结束工作流，绝对不允许再打回给 Writer！\n"
        "3. 见好就收：如果 Writer 已经输出了最终版本的报告且经过了一次审查，请选择 'FINISH'。"
        "4. 🚨 错误熔断机制 (最重要)：仔细阅读聊天记录，如果发现 Researcher 汇报了包含『错误』、『Error』、『超时』等字眼，说明底层工具已崩溃。【绝对不允许】再把任务派给 Researcher！你应该直接让 Writer 用现有的残缺数据写报告，或者直接选择 'FINISH'。"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        ("system", "请基于以上最新进度，做出下一步的调度决策。如果任务已全部完成或审查已通过，必须输出 FINISH。")
    ])

    # 强制 LLM 输出符合 A2A 协议的结构化决策
    supervisor_chain = prompt | llm.with_structured_output(
        SupervisorDecision,
        method="function_calling"
    )

    def supervisor_node(state: ResearchState) -> dict:
        print("\n👔 [Supervisor] 正在审视全局进度，思考下一步调度...")

        # 提取对话历史供主管参考
        decision: SupervisorDecision = supervisor_chain.invoke({
            "messages": state["messages"]
        })

        print(f"👔 [Supervisor] 决定指派给: {decision.next_agent}")
        if decision.next_agent == "FINISH":
            print("👔 [Supervisor] 任务圆满完成，结束图流转！")

        return {
            "next": decision.next_agent,
            "current_instruction": decision.instruction
        }

    return supervisor_node