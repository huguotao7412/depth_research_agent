# app/api/routes.py
import os
import shutil
import asyncio
import json
import traceback
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import List, Optional
from app.agents.graph import build_multi_agent_graph
from app.core.llm_factory import get_llm
from langgraph.errors import GraphRecursionError
from langchain_core.messages import HumanMessage, AIMessage
from app.rag.retrievers import get_retriever
from app.core.workspace import get_workspaces, create_workspace

router = APIRouter()
llm = get_llm(model_type="main", temperature=0.0)
research_agent = build_multi_agent_graph(llm)

@router.get("/workspaces", summary="获取所有工作区")
def list_workspaces():
    return get_workspaces()

@router.post("/workspaces", summary="创建新工作区")
def add_new_workspace():
    new_id = create_workspace()
    return {"workspace_id": new_id}

class ResearchRequest(BaseModel):
    query: str
    workspace_id: str
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
    pass


@router.post("/research/stream", summary="流式提交深度研究任务 (SSE)")
async def run_research_stream(request: ResearchRequest):
    async def event_generator():
        # 🚨 核心改造 1：启用 Checkpointer 后，无需手动拼接全量 chat_history
        # 我们只向图引擎喂入用户当次发送的最新一条 Query 即可
        messages_input = [HumanMessage(content=request.query)]

        inputs = {
            "user_query": request.query,
            "messages": messages_input,
            "raw_docs_path": f"data/{request.workspace_id}/raw_docs",
            "vector_db_path": f"data/{request.workspace_id}/vector_db/faiss_index"
        }

        # 🚨 核心改造 2：使用 workspace_id 作为 thread_id 激活沙盒记忆
        thread_id = request.workspace_id if request.workspace_id else "default_thread"
        config = {
            "configurable": {"thread_id": thread_id},
            "recursion_limit": 50
        }

        try:
            # 🚨 核心改造 3：将带有 thread_id 的 config 传入 astream
            async for output in research_agent.astream(inputs, config=config):
                for node_name, state_update in output.items():
                    # 拦截 MemoryManager 节点的流转信息，让其在后台静默运行，不干扰前端 UI
                    if node_name == "MemoryManager":
                        continue

                    event_data = {"node": node_name, "state_update": state_update}
                    yield f"data: {json.dumps(jsonable_encoder(event_data), ensure_ascii=False)}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            traceback.print_exc()
            yield f"data: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.post("/docs/upload", summary="上传文献并异步建库")
async def upload_document(file: UploadFile = File(...), workspace_id: str = Form(...)):
    docs_dir = f"data/{workspace_id}/raw_docs"
    vector_db_path = f"data/{workspace_id}/vector_db/faiss_index"
    os.makedirs(docs_dir, exist_ok=True)

    file_path = os.path.join(docs_dir, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    retriever = get_retriever(raw_docs_path=docs_dir, vector_db_path=vector_db_path)
    asyncio.create_task(retriever.aingest_documents())

    return {"status": "success", "message": "上传成功，后台正在解析建库"}


@router.delete("/docs/{filename}", summary="删除文献并重建索引")
async def delete_document(filename: str, workspace_id: str):
    docs_dir = f"data/{workspace_id}/raw_docs"
    vector_db_path = f"data/{workspace_id}/vector_db/faiss_index"

    file_path = os.path.join(docs_dir, filename)
    if os.path.exists(file_path):
        os.remove(file_path)

        if os.path.exists(vector_db_path):
            shutil.rmtree(vector_db_path)

        for ext in ["_bm25.pkl", "_kv_store.pkl"]:
            cache_file = vector_db_path + ext
            if os.path.exists(cache_file):
                os.remove(cache_file)

        retriever = get_retriever(raw_docs_path=docs_dir, vector_db_path=vector_db_path)
        asyncio.create_task(retriever.aingest_documents())

        return {"status": "success"}

    raise HTTPException(status_code=404, detail="文件不存在")