import json
import traceback  # 🚨 新增：用于打印异常堆栈
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.encoders import jsonable_encoder # 🚨 新增：防止 JSON 序列化报错
from pydantic import BaseModel, Field
from typing import List, Optional
from app.agents.graph import build_multi_agent_graph
from app.core.llm_factory import get_llm
from langgraph.errors import GraphRecursionError

router = APIRouter()
print("⏳ 正在挂载 LangGraph Multi-Agent 引擎...")

# ✅ 修正 1：必须初始化 LLM 并调用函数实例化图！
llm = get_llm(model_type="main", temperature=0.0)
research_agent = build_multi_agent_graph(llm)

class ResearchRequest(BaseModel):
    query: str
    chat_history: Optional[List[dict]] = Field(default=[], description="前端传来的历史对话记录")
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
        messages_input = []
        for msg in request.chat_history:  # ✅ 注入历史记忆
            role = "user" if msg["role"] == "user" else "assistant"
            messages_input.append((role, msg["content"]))

        # 将本次的新问题也加进去
        messages_input.append(("user", request.query))
        # ✅ 修正 2：对齐 ResearchState，加入 messages 字段激活流转
        inputs = {
            "user_query": request.query,
            "messages": messages_input,
            "raw_docs_path": request.raw_docs_path,
            "vector_db_path": request.vector_db_path
        }

        try:
            async for output in research_agent.astream(inputs, config={"recursion_limit": 15}):
                for node_name, state_update in output.items():
                    event_data = {
                        "node": node_name,
                        "state_update": state_update
                    }
                    safe_event_data = jsonable_encoder(event_data)
                    yield f"data: {json.dumps(safe_event_data, ensure_ascii=False)}\n\n"

            yield "data: [DONE]\n\n"


        except GraphRecursionError:

            # 🚨 提升 2: 优雅地捕获死循环并推送到前端

            error_msg = "⚠️ 团队讨论超过15轮，触发强制熔断保护。请尝试细化您的研究问题。"

            print(f"\n❌ {error_msg}")

            yield f"data: {json.dumps({'error': error_msg}, ensure_ascii=False)}\n\n"


        except Exception as e:

            # 原本的兜底异常处理

            print("\n❌ 代理流转期间发生严重错误:")

            traceback.print_exc()

            yield f"data: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")