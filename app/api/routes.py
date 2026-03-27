import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List, Optional
from app.agents.graph import build_omni_research_graph

router = APIRouter()
print("⏳ 正在挂载 LangGraph 智能体引擎...")
research_agent = build_omni_research_graph()


class ResearchRequest(BaseModel):
    query: str
    domain: Optional[str] = Field(default="通用学术领域", description="研究领域")
    glossary: Optional[List[str]] = Field(default=[], description="核心术语列表")
    raw_docs_path: Optional[str] = Field(default="data/raw_docs", description="PDF存放路径")
    vector_db_path: Optional[str] = Field(default="data/vector_db/faiss_index", description="索引存放路径")


# 【保留原有普通接口，防止旧代码报错】
class ResearchResponse(BaseModel):
    status: str
    final_report: str
    sub_questions: List[str]
    retrieved_docs_count: int
    feedback_log: str


@router.post("/research", response_model=ResearchResponse, summary="提交深度研究任务")
async def run_research(request: ResearchRequest):
    # ... 原有代码保持不变 ...
    try:
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


# ==================== 【新增：SSE 流式接口】 ====================
@router.post("/research/stream", summary="流式提交深度研究任务 (SSE)")
async def run_research_stream(request: ResearchRequest):
    """通过 Server-Sent Events 实时推送 Agent 的思考状态"""

    async def event_generator():
        inputs = {
            "query": request.query,
            "domain_config": {
                "domain": request.domain,
                "glossary": request.glossary,
                "raw_docs_path": request.raw_docs_path,
                "vector_db_path": request.vector_db_path
            }
        }

        try:
            # astream() 会在图中每一个节点执行完毕后，产出状态更新
            async for output in research_agent.astream(inputs):
                # output 是一个字典，格式如：{"节点名称": {"状态增量"}}
                for node_name, state_update in output.items():
                    # 组装我们要发给前端的数据包
                    event_data = {
                        "node": node_name,
                        "state_update": state_update
                    }
                    # 按照 SSE 规范格式化字符串并发送
                    yield f"data: {json.dumps(event_data, ensure_ascii=False)}\n\n"

            # 整个图执行完毕，发送结束信号
            yield "data: [DONE]\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")