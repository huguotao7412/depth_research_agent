# app/agents/workers/planner.py
import json
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field
from langchain_core.messages import AIMessage
from app.core.state import ResearchState
from app.core.llm_factory import get_llm

# 🚨 引入显式长期记忆库
from app.core.memory_store import get_profile

class ResearchPlan(BaseModel):
    steps: list[str] = Field(description="拆解后的具体子任务列表，每个任务必须独立且包含明确的检索意图")
    reasoning: str = Field(description="任务分解的思考过程")

def planner_node(state: ResearchState) -> dict:
    llm = get_llm(model_type="main", temperature=0.2)
    instruction = state.get("current_instruction")
    task_desc = instruction.task_description if instruction and hasattr(instruction, 'task_description') else "制定详细的文献调研任务分解计划"

    # 🚨 获取当前工作区的长期显式偏好 (JSON)
    workspace_id = state.get("workspace_id", "default")
    profile = get_profile(workspace_id)

    # 构建基础系统提示词
    system_prompt = (
        "你是一个顶尖的学术规划与分解大脑 (Planner)。\n"
        "你的核心职责是进行【任务分解 (Task Decomposition)】。\n"
        "你需要根据主管的指令，将复杂的调研需求拆解为多个独立、清晰的子任务。这些子任务随后将分配给多个 Actor 智能体进行【底层并行执行 (Run in Parallel)】。\n\n"
        "【拆解原则】\n"
        "1. 独立解耦：子任务之间不应有严格的先后依赖，确保它们可以完全同时并发检索。\n"
        "2. 动态深度：根据用户问题的复杂程度，动态决定子任务的数量（通常 2-5 个），用户问的精准时，子任务数量少，问的笼统时，子任务数量多，不要拘泥于固定的数量。\n"
        "3. 动作导向：每个子任务描述不应只是一个标题（如“研究背景”），而必须是一个具体的检索指令（如“检索并提取近三年关于毫米波雷达生命体征监测的信噪比优化算法数据”）。\n"
        "必须严格输出 JSON 格式的结构化数据。"
    )

    # 🚨 动态注入心智：如果有设定的偏好，贴在 Planner 脑门上
    if profile:
        system_prompt += (
            f"\n\n🧠 【Boss 的专属研究偏好 (Profile)】:\n"
            f"{json.dumps(profile, ensure_ascii=False, indent=2)}\n"
            "(请在拆解子任务时，自动体现并侧重 Boss 的研究偏好，隐式加入相关要求。)"
        )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        ("user", "主管的具体指令：{instruction}\n请输出详细的任务分解计划。")
    ])

    chain = prompt | llm.with_structured_output(
        ResearchPlan,
        method="function_calling"
    )

    try:
        result = chain.invoke({
            "messages": state["messages"],
            "instruction": task_desc
        })

        if result is None or not hasattr(result, 'steps'):
            raise ValueError("大模型未能成功生成合规的 JSON 结构。")

        plan_text = "\n".join([f"任务 {i + 1}: {step}" for i, step in enumerate(result.steps)])
        response_msg = AIMessage(
            content=f"【Planner 汇报】任务分解完成。\n思考过程：{result.reasoning}\n\n已下发并发子任务：\n{plan_text}",
            name="Planner"
        )
        return {
            "messages": [response_msg],
            "research_plan": result.steps
        }
    except Exception as e:
        print(f"Planner 节点执行失败: {e}")
        error_msg = AIMessage(content=f"【Planner 报错】无法分解任务，错误信息: {str(e)}。建议重试。", name="Planner")
        return {"messages": [error_msg]}