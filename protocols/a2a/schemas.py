# protocols/a2a/schemas.py
import json
from pydantic import BaseModel, Field, model_validator
from typing import List, Literal, Optional, Any

# 定义系统内所有的 Agent 角色
AgentRole = Literal["Planner", "Researcher", "Reviewer", "Writer", "DailyQA", "FINISH"]

class AgentTaskInstruction(BaseModel):
    """Supervisor 发送给 Worker 的标准化任务指令"""
    target_agent: AgentRole = Field(description="任务接收方")
    task_description: str = Field(description="具体的任务描述与要求")
    context_required: Optional[str] = Field(description="完成该任务所需的上下文摘要")

class SupervisorDecision(BaseModel):
    """Supervisor 的决策输出协议"""
    next_agent: AgentRole = Field(description="下一个需要调用的 Agent")
    reasoning: str = Field(description="为什么选择这个 Agent 的思考过程")
    instruction: Optional[AgentTaskInstruction] = Field(description="给下一个 Agent 的具体指令")

    # 👇 新增：前置校验器，专门修复大模型嵌套 JSON 字符串化的问题
    @model_validator(mode='before')
    @classmethod
    def parse_instruction_if_string(cls, data: Any) -> Any:
        if isinstance(data, dict):
            instruction_val = data.get("instruction")
            # 如果发现大模型把 instruction 输出成了字符串
            if isinstance(instruction_val, str):
                try:
                    # 手动将其反序列化为字典
                    data["instruction"] = json.loads(instruction_val)
                except json.JSONDecodeError:
                    pass # 如果解析失败，原样放行，让 Pydantic 抛出标准错误
        return data