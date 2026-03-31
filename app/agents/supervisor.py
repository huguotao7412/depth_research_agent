# app/agents/supervisor.py
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from protocols.a2a.schemas import SupervisorDecision
from app.core.state import ResearchState


def create_supervisor_node(llm: ChatOpenAI):
    system_prompt = (
        "你是一个顶尖学术研究团队的主管 (Supervisor)。"
        "你的目标是通过协调以下团队成员来完成用户的最终研究任务。\n\n"
        "【标准工作流 (SOP) - 必须严格按顺序流转】:\n"
        "第 1 步: Planner - 负责拆解复杂的学术问题，制定研究大纲。\n"
        "第 2 步: Researcher - 在大纲制定后，负责检索资料和数据。\n"
        "第 3 步: Writer - 在数据收集完成后，【必须】由它负责基于数据撰写初始学术报告。\n"
        "第 4 步: Reviewer - 在 Writer 产出初稿后，负责审查逻辑和事实准确性。\n\n"
        "⚠️ 【强制调度纪律 - 必须严格遵守】：\n"
        "1. 绝对不能跳步：在 Researcher 收集完数据后，下一步【必须】是 Writer！绝对不允许在没有草稿的情况下直接指派 Reviewer！\n"
        "2. 结束条件 (FINISH)：仔细阅读最近的聊天记录，只有当【Writer 已经撰写了初稿】，并且【Reviewer 的最新反馈中明确包含 'APPROVED' 或 '通过'】时，你才能直接选择 'FINISH' 结束工作流。如果没有草稿产出，绝对不能 FINISH！\n"
        "3. 🚨 错误熔断：如果发现 Researcher 汇报了包含『错误』、『Error』、『超时』等字眼，你应该直接让 Writer 用现有的残缺数据写报告，不要再让 Researcher 尝试。"
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
            print("👔 [Supervisor] 任务流转结束！")

        return {
            "next": decision.next_agent,
            "current_instruction": decision.instruction
        }

    return supervisor_node