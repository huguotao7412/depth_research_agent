# app/api/server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from protocols.mcp.client import get_mcp_tools_and_client
from app.rag.retrievers import get_retriever
from contextlib import asynccontextmanager

from app.core.workspace import init_workspaces # 🚨 引入工作区初始化模块

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n🚀 [Lifespan] 后端服务启动中：正在后台预热长耗时组件...")

    init_workspaces() # 🚨 启动时确保全局注册表存在

    # 1. 预热 MCP 客户端 (瞬间拉起 Node.js 进程)
    try:
        await get_mcp_tools_and_client()
        print("✅ [Lifespan] MCP 联邦检索服务器预加载完成！")
    except Exception as e:
        print(f"⚠️ [Lifespan] MCP 预热失败，将在首次检索时重试: {e}")

    # 🚨 2. 取消对本地 FAISS 的启动强制预热，因为我们现在有无限个潜在工作区。
    # Retriever 工厂会在用户首次提问或上传文献时，按需毫秒级拉起对应工作区的内存索引。

    yield
    print("\n🛑 [Lifespan] 后端服务正在关闭...")

def create_app() -> FastAPI:
    # 1. 实例化 FastAPI
    app = FastAPI(
        title="DepthResearch-Agent API",
        description="可插拔式通用深度研究智能体引擎 API 服务",
        version="1.0.0"
    )

    # 2. 配置跨域 (CORS) - 允许前端页面直接调用
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # 生产环境建议替换为具体的前端域名
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 3. 注册 API 路由，并带上统一的 /api/v1 前缀
    app.include_router(router, prefix="/api/v1", tags=["Research"])

    return app