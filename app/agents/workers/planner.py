# app/agents/workers/planner.py
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langchain_core.messages import AIMessage
from app.core.state import ResearchState


class ResearchPlan(BaseModel):
    steps: list[str] = Field(description="拆解后的具体研究步骤或大纲列表")
    reasoning: str = Field(description="为什么这样拆解的思考过程")


def planner_node(state: ResearchState) -> dict:
    llm = ChatOpenAI(model="deepseek-chat", temperature=0.2)
    instruction = state.get("current_instruction")
    task_desc = instruction.task_description if instruction else "制定详细的文献调研与写作大纲"

    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个严谨的学术规划师 (Planner)。"
                   "你的任务是根据主管的指令和用户原始需求，拆解出具体的研究子任务。\n"
                   "例如，在面对如“毫米波雷达血压预测技术的挑战与对策”这类交叉学科课题时，"
                   "你需要将其拆分为：1. 原理剖析；2. 现有痛点（如运动伪影）；3. 算法对策；4. 前景展望等具体步骤。"),
        MessagesPlaceholder(variable_name="messages"),
        ("user", "主管的具体指令：{instruction}\n请输出详细的研究计划。")
    ])

    chain = prompt | llm.with_structured_output(
        ResearchPlan,
        method="function_calling"
    )
    result = chain.invoke({
        "messages": state["messages"],
        "instruction": task_desc
    })

    # 格式化输出消息，反馈给 Supervisor 审查
    plan_text = "\n".join([f"{i + 1}. {step}" for i, step in enumerate(result.steps)])
    response_msg = AIMessage(
        content=f"【规划完成】\n思考过程：{result.reasoning}\n\n研究计划如下：\n{plan_text}",
        name="Planner"
    )

    return {
        "messages": [response_msg],
        "research_plan": result.steps  # 更新共享状态，供后续节点使用
    }