from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.agents.graph import build_omni_research_graph

# 创建一个 API 路由器
router = APIRouter()

# 1. 在内存中全局初始化一次 Agent 状态机，避免每次请求都重新编译
print("⏳ 正在挂载 LangGraph 智能体引擎...")
research_agent = build_omni_research_graph()


# 2. 定义 API 的请求体结构 (Pydantic Schema)
class ResearchRequest(BaseModel):
    query: str


# 3. 定义 API 的响应体结构
class ResearchResponse(BaseModel):
    status: str
    final_report: str
    sub_questions: List[str]
    retrieved_docs_count: int
    feedback_log: str


@router.post("/research", response_model=ResearchResponse, summary="提交深度研究任务")
async def run_research(request: ResearchRequest):
    """
    接收用户的研究问题，触发多智能体 RAG 工作流，返回最终报告。
    """
    try:
        inputs = {"query": request.query}

        # 使用 .invoke() 同步执行整个图的流转，直到到达 END 节点
        # 注意：在真实的长时间执行场景下，这里可以改成异步或者流式输出(Streaming)
        final_state = research_agent.invoke(inputs)

        return ResearchResponse(
            status="success",
            final_report=final_state.get("final_report", "报告生成失败"),
            sub_questions=final_state.get("sub_questions", []),
            retrieved_docs_count=len(final_state.get("documents", [])),
            feedback_log=final_state.get("review_feedback", "")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent 执行出错: {str(e)}")