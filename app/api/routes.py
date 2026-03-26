from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from app.agents.graph import build_omni_research_graph

router = APIRouter()
print("⏳ 正在挂载 LangGraph 智能体引擎...")
research_agent = build_omni_research_graph()

# 增加可选的领域配置参数
class ResearchRequest(BaseModel):
    query: str
    domain: Optional[str] = Field(default="通用学术领域", description="研究领域")
    glossary: Optional[List[str]] = Field(default=[], description="核心术语列表")
    raw_docs_path: Optional[str] = Field(default="data/raw_docs", description="PDF存放路径")
    vector_db_path: Optional[str] = Field(default="data/vector_db/faiss_index", description="索引存放路径")

class ResearchResponse(BaseModel):
    status: str
    final_report: str
    sub_questions: List[str]
    retrieved_docs_count: int
    feedback_log: str

@router.post("/research", response_model=ResearchResponse, summary="提交深度研究任务")
async def run_research(request: ResearchRequest):
    try:
        # 将传入的参数组装并传递给初始 State
        inputs = {
            "query": request.query,
            "domain_config": {
                "domain": request.domain,
                "glossary": request.glossary,
                "raw_docs_path": request.raw_docs_path,
                "vector_db_path": request.vector_db_path
            }
        }
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