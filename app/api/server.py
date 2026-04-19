# app/api/server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from contextlib import asynccontextmanager
from protocols.mcp.client import mcp_lifecycle_manager

from app.core.workspace import init_workspaces # 🚨 引入工作区初始化模块


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n🚀 [Lifespan] 后端服务启动中...")
    init_workspaces()

    # 🚨 核心修复：使用 async with 保证子进程生命周期
    async with mcp_lifecycle_manager() as (mcp_client, mcp_tools):
        yield  # 此时应用正在运行，MCP 进程存活

    # 退出 yield 后，mcp_lifecycle_manager 会自动清理进程
    print("\n🛑 [Lifespan] 后端服务已平滑关闭。")

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