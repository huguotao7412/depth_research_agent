# app/agents/supervisor.py
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from protocols.a2a.schemas import SupervisorDecision, AgentTaskInstruction # 🚨 引入 AgentTaskInstruction
from app.core.state import ResearchState

def create_supervisor_node(llm: ChatOpenAI):
    def supervisor_node(state: ResearchState) -> dict:
        print("\n👔 [Supervisor] 正在审视全局进度，思考下一步调度...")
        session_summary = state.get("session_summary", "")
        messages = state.get("messages", [])
        last_agent = messages[-1].name if messages and hasattr(messages[-1], "name") else "User"

        system_prompt = f"""你是一个顶尖学术研究团队的主管 (Supervisor)。
        你需要根据当前进度，灵活调度团队成员。作为系统的入口网关，你必须决定当前任务走“⚡快系统”还是“🐢慢系统”。

        【当前进度定位】: 上一步刚刚完成工作的是 [{last_agent}]。

        【动态工作流 (Dynamic Workflow) - 团队职责】:
        1. ⚡ 快系统 (DailyQA): 专职处理基础概念解释、名词解释、代码语法问答等简单指令（如“什么是向量数据库”、“解释一下残差网络”）。【特点：不检索文献，极速响应】。
        2. 🐢 慢系统 (深度研究):
           - Planner: 负责【任务分解 (Task Decomposition)】，将复杂大目标拆解为独立子任务。
           - Researcher (Actor Cluster): 负责【并行加速】，接收子任务后，同时实例化多个 Actor 智能体并行运行各自的 RAG 和网页检索。
           - Writer: 基于收集到的数据撰写、扩充学术报告。
           - Reviewer: 审查初稿的逻辑严密性与引用规范。

        🔄 【核心调度路由逻辑 - 绝对铁律】：
        1. 🚀 初始网关分流 (当 {last_agent} 为 User 时)：
           - 如果用户只是问基础知识、寻求简单解释，你【必须】将任务指派给 `DailyQA`。
           - 如果用户要求“调研文献”、“写综述”、“对比分析”等复杂研究任务，你【必须】将任务指派给 `Planner` 启动慢系统流转。
        2. ⚡ 快系统闭环：如果上一步是 `DailyQA`，说明轻量级回答已生成，你【必须】立刻输出 `FINISH`。
        3. 🐢 慢系统闭环推进：Planner -> Researcher -> Writer -> Reviewer。
        4. 审查打回：Reviewer 若提出事实不足，唤醒 Researcher；若提出润色建议，唤醒 Writer。

        ✅ 【结束条件 (FINISH)】:
        只有当 `DailyQA` 刚执行完毕，或者 `Reviewer` 的审查意见中明确包含 'APPROVED' 时，才能选择 'FINISH' 结束！
        """

        if session_summary:
            system_prompt += f"\n\n🧠 【前置对话情境摘要】:\n{session_summary}\n(请在理解用户意图和分配任务时，务必参考上述背景历史)"

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