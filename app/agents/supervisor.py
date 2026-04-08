# app/agents/supervisor.py
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from protocols.a2a.schemas import SupervisorDecision, AgentTaskInstruction # 🚨 引入 AgentTaskInstruction
from app.core.state import ResearchState

def create_supervisor_node(llm: ChatOpenAI):
    def supervisor_node(state: ResearchState) -> dict:
        print("\n👔 [Supervisor] 正在审视全局进度，思考下一步调度...")

        messages = state.get("messages", [])
        last_agent = messages[-1].name if messages and hasattr(messages[-1], "name") else "User"

        system_prompt = f"""你是一个顶尖学术研究团队的主管 (Supervisor)。
你的目标是通过协调以下团队成员来完成深度学术调研与写作。

【当前进度定位】: 上一步刚刚完成工作的是 [{last_agent}]。

【动态工作流 (Dynamic Workflow) - 团队职责】:
- Planner: 拆解复杂问题，制定大纲（仅在初始阶段或大纲需要彻底推翻时调用）。
- Researcher: 负责检索资料、提取核心数据和证据来源。
- Writer: 基于收集到的数据撰写、扩充或修改学术报告。
- Reviewer: 审查初稿的逻辑严密性、事实准确性和引用规范。

🔄 【核心调度逻辑：深度研究闭环】：
1. 常规推进：Planner 规划 -> Researcher 检索 -> Writer 撰写 -> Reviewer 审查。
2. 缺失打回（数据层）：如果 Reviewer 提出核心数据缺失或事实不足，你【必须】唤醒 Researcher 进行定向补充检索！
3. 润色打回（文本层）：如果 Reviewer 仅提出结构调整或文字润色建议，请唤醒 Writer 修改。
4. 异常熔断：如果 Researcher 遇到网络瘫痪或致命报错，让 Writer 尽力用残缺数据产出报告。

✅ 【结束条件 (FINISH)】:
只有当 Reviewer 最新的审查意见中明确包含 'APPROVED' 或 '通过' 时，你才能选择 'FINISH' 结束工作流。绝不可提前结束！
"""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
            ("system", "请基于以上最新进度，做出下一步的调度决策。如果审查已通过，必须输出 FINISH。")
        ])

        supervisor_chain = prompt | llm.with_structured_output(
            SupervisorDecision,
            method="function_calling"
        )

        try:
            decision: SupervisorDecision = supervisor_chain.invoke({
                "messages": messages
            })
        except Exception as e:
            print(f"⚠️ [Supervisor] 模型格式输出崩溃或解析异常: {str(e)}")
            decision = None  # 强制进入下方的兜底降级流程

        # ==========================================
        # 🚨 核心修复：应对 GLM-4-Flash 等模型格式输出失败
        # ==========================================
        if decision is None:
            print("⚠️ [Supervisor] 警告：大模型未能输出有效调度指令(返回了 None)。触发兜底降级...")
            return {
                "next": "Planner",
                "current_instruction": AgentTaskInstruction(
                    target_agent="Planner",
                    task_description="由于调度解析异常，请重新评估当前进度并制定下一步计划。",
                    context_required=""
                )
            }

        print(f"👔 [Supervisor] 决定指派给: {decision.next_agent}")
        if decision.next_agent == "FINISH":
            print("👔 [Supervisor] 任务流转结束！")

        return {
            "next": decision.next_agent,
            "current_instruction": decision.instruction
        }

    return supervisor_node