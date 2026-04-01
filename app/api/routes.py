import json
import traceback  # 🚨 新增：用于打印异常堆栈
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.encoders import jsonable_encoder # 🚨 新增：防止 JSON 序列化报错
from pydantic import BaseModel, Field
from typing import List, Optional
from langchain_openai import ChatOpenAI
from app.agents.graph import build_multi_agent_graph
from app.core.llm_factory import get_llm

router = APIRouter()
print("⏳ 正在挂载 LangGraph Multi-Agent 引擎...")

# ✅ 修正 1：必须初始化 LLM 并调用函数实例化图！
llm = get_llm(model_type="main", temperature=0.0)
research_agent = build_multi_agent_graph(llm)

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
    # (省略普通接口代码，保持你之前的修改即可)
    pass

@router.post("/research/stream", summary="流式提交深度研究任务 (SSE)")
async def run_research_stream(request: ResearchRequest):
    async def event_generator():
        # ✅ 修正 2：对齐 ResearchState，加入 messages 字段激活流转
        inputs = {
            "user_query": request.query,
            "messages": [("user", request.query)],
            "raw_docs_path": request.raw_docs_path,
            "vector_db_path": request.vector_db_path
        }

        try:
            async for output in research_agent.astream(inputs):
                for node_name, state_update in output.items():
                    event_data = {
                        "node": node_name,
                        "state_update": state_update
                    }
                    # ✅ 修正 3：使用 jsonable_encoder 安全转换复杂对象 (如 AIMessage, Pydantic)
                    safe_event_data = jsonable_encoder(event_data)
                    yield f"data: {json.dumps(safe_event_data, ensure_ascii=False)}\n\n"

            yield "data: [DONE]\n\n"

        except Exception as e:
            # 🚨 修正 4：必须打印堆栈，否则后端假死你根本不知道错在哪！
            print("\n❌ 代理流转期间发生严重错误:")
            traceback.print_exc()
            yield f"data: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")