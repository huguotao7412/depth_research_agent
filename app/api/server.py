from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

def create_app() -> FastAPI:
    # 1. 实例化 FastAPI
    app = FastAPI(
        title="OmniResearch-Agent API",
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