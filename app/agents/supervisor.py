# app/agents/supervisor.py
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from protocols.a2a.schemas import SupervisorDecision
from app.core.state import ResearchState


def create_supervisor_node(llm: ChatOpenAI):
    def supervisor_node(state: ResearchState) -> dict:
        print("\n👔 [Supervisor] 正在审视全局进度，思考下一步调度...")

        # 1. 获取上一个发言的 Agent 名称，用于动态提示 LLM
        messages = state.get("messages", [])
        last_agent = messages[-1].name if messages and hasattr(messages[-1], "name") else "User"

        # 2. 动态注入当前状态，让 LLM 明确知道自己在哪一步
        system_prompt = f"""你是一个顶尖学术研究团队的主管 (Supervisor)。
你的目标是通过协调以下团队成员来完成用户的最终研究任务。

【当前进度定位】: 上一步刚刚完成工作的是 [{last_agent}]。

【标准工作流 (SOP) - 必须严格按顺序流转】:
第 1 步: Planner - 负责拆解复杂的学术问题，制定研究大纲。
第 2 步: Researcher - 在大纲制定后，负责检索资料和数据。
第 3 步: Writer - 在 Researcher 收集完成后，【必须】由它负责基于数据撰写初始学术报告。
第 4 步: Reviewer - 在 Writer 产出初稿后，负责审查逻辑和事实准确性。

⚠️ 【强制调度纪律 - 必须严格遵守】：
1. 绝对不能跳步：如果上一步是 Researcher，下一步【必须】是 Writer！绝对不允许指派 Reviewer！
2. 结束条件 (FINISH)：仔细阅读最近的聊天记录，只有当【Writer 已经撰写了初稿】，并且【Reviewer 的最新反馈中明确包含 'APPROVED' 或 '通过'】时，你才能直接选择 'FINISH' 结束工作流。
3. 🚨 错误熔断：如果发现 Researcher 汇报了包含『错误』、『Error』、『超时』等字眼，你应该直接让 Writer 用现有的残缺数据写报告。
"""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
            ("system", "请基于以上最新进度，做出下一步的调度决策。如果任务已全部完成或审查已通过，必须输出 FINISH。")
        ])

        supervisor_chain = prompt | llm.with_structured_output(
            SupervisorDecision,
            method="function_calling"
        )

        # 请求大模型做出决策
        decision: SupervisorDecision = supervisor_chain.invoke({
            "messages": messages
        })

        # ==========================================
        # 🛡️ 3. 代码级防御性拦截 (拦截 LLM 幻觉)
        # ==========================================
        if last_agent == "Researcher" and decision.next_agent == "Reviewer":
            print("   [System] ⚠️ 检测到 LLM 路由违规，强制纠正: Researcher -> Writer")
            decision.next_agent = "Writer"

        print(f"👔 [Supervisor] 决定指派给: {decision.next_agent}")
        if decision.next_agent == "FINISH":
            print("👔 [Supervisor] 任务流转结束！")

        return {
            "next": decision.next_agent,
            "current_instruction": decision.instruction
        }

    return supervisor_node