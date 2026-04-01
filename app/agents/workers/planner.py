# app/agents/workers/planner.py
import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langchain_core.messages import AIMessage
from app.core.state import ResearchState
from app.core.llm_factory import get_llm


class ResearchPlan(BaseModel):
    steps: list[str] = Field(description="拆解后的具体研究步骤或大纲列表")
    reasoning: str = Field(description="为什么这样拆解的思考过程")


def planner_node(state: ResearchState) -> dict:
    llm = get_llm(model_type="fast", temperature=0.2)
    instruction = state.get("current_instruction")
    # 如果 instruction 是对象，防止它为 None 时报错
    task_desc = instruction.task_description if instruction and hasattr(instruction,
                                                                        'task_description') else "制定详细的文献调研与写作大纲"

    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个严谨的学术规划师 (Planner)。"
                   "你的任务是根据主管的指令和用户原始需求，拆解出具体的研究子任务。\n"
                   "【拆解原则】\n"
                   "1. 动态深度：根据用户问题的复杂程度，动态决定子任务的数量（通常 2-5 个），用户问的精准时，子任务数量少，问的笼统时，子任务数量多，不要拘泥于固定的数量。\n"
                   "2. 动态风格适应（🌟关键）：如果用户的任务是『文献综述』、『国内外研究现状』，请【绝对不要】使用“1.研究背景 2.研究意义 3.预期成果”这种空洞的八股文框架！你应该按照『技术发展的不同阶段』、『不同的技术流派』来拆解大纲。\n"
                   "3. 结构严谨：遵循 MECE 原则，确保子任务之间相互独立且完全穷尽。\n"
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
        }