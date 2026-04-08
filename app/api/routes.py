import os
import shutil
import asyncio
import json
import traceback  # 🚨 新增：用于打印异常堆栈
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.encoders import jsonable_encoder # 🚨 新增：防止 JSON 序列化报错
from pydantic import BaseModel, Field
from typing import List, Optional
from app.agents.graph import build_multi_agent_graph
from app.core.llm_factory import get_llm
from langgraph.errors import GraphRecursionError
from langchain_core.messages import HumanMessage, AIMessage
from app.rag.retrievers import get_retriever

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
            if msg["role"] == "user":
                messages_input.append(HumanMessage(content=msg["content"]))
            else:
                agent_name = msg.get("name", "Assistant")
                messages_input.append(AIMessage(content=msg["content"], name=agent_name))

        messages_input.append(HumanMessage(content=request.query))
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


# 🚨 新增：文献上传与异步建库接口
@router.post("/docs/upload", summary="上传文献并异步建库")
async def upload_document(file: UploadFile = File(...)):
    docs_dir = "data/raw_docs"
    os.makedirs(docs_dir, exist_ok=True)
    file_path = os.path.join(docs_dir, file.filename)

    # 1. 保存文件
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 2. 触发后台异步建库，不阻塞前端响应
    retriever = get_retriever()
    asyncio.create_task(retriever.aingest_documents())

    return {"status": "success", "message": f"{file.filename} 上传成功，后台正在解析建库"}


# 🚨 新增：文献删除与缓存清理接口
@router.delete("/docs/{filename}", summary="删除文献并重建索引")
async def delete_document(filename: str):
    file_path = os.path.join("data/raw_docs", filename)
    if os.path.exists(file_path):
        os.remove(file_path)

        # 清理旧索引目录
        index_dir = "data/vector_db/faiss_index"
        if os.path.exists(index_dir):
            shutil.rmtree(index_dir)

        # 清理同级缓存文件
        for ext in ["_bm25.pkl", "_kv_store.pkl"]:
            cache_file = index_dir + ext
            if os.path.exists(cache_file):
                os.remove(cache_file)

        # 触发后台重新建库
        retriever = get_retriever()
        asyncio.create_task(retriever.aingest_documents())

        return {"status": "success", "message": "删除成功，索引正在后台重建"}

    raise HTTPException(status_code=404, detail="文件不存在")