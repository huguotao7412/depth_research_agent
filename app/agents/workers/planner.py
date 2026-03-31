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
    # 如果 instruction 是对象，防止它为 None 时报错
    task_desc = instruction.task_description if instruction and hasattr(instruction,
                                                                        'task_description') else "制定详细的文献调研与写作大纲"

    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个严谨的学术规划师 (Planner)。"
                   "你的任务是根据主管的指令和用户原始需求，拆解出具体的研究子任务。\n"
                   "例如：将其拆分为：1. 原理剖析；2. 现有痛点；3. 算法对策等。\n"
                   "必须严格输出 JSON 格式的结构化数据。"),
        MessagesPlaceholder(variable_name="messages"),
        ("user", "主管的具体指令：{instruction}\n请输出详细的研究计划。")
    ])

    chain = prompt | llm.with_structured_output(
        ResearchPlan,
        method="function_calling"
    )

    # 增加异常捕捉，防止 LLM API 抽风导致静默挂起
    try:
        result = chain.invoke({
            "messages": state["messages"],
            "instruction": task_desc
        })

        plan_text = "\n".join([f"{i + 1}. {step}" for i, step in enumerate(result.steps)])
        response_msg = AIMessage(
            content=f"【Planner 汇报】规划完成。\n思考过程：{result.reasoning}\n\n研究计划如下：\n{plan_text}",
            name="Planner"
        )
        return {
            "messages": [response_msg],
            "research_plan": result.steps
        }
    except Exception as e:
        print(f"Planner 节点执行失败: {e}")
        # 返回一个降级信息让流程继续或让主管知道出错
        error_msg = AIMessage(content=f"【Planner 报错】无法生成计划，错误信息: {str(e)}", name="Planner")
        return {
            "messages": [error_msg],
            "research_plan": []
        }