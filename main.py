import os
from dotenv import load_dotenv
load_dotenv()

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  # 【关键修复】防止底层 C++ 库冲突导致闪退

import uvicorn

# 2. 导入刚刚写好的 app 工厂函数
from app.api.server import create_app

# 3. 创建 FastAPI 实例
app = create_app()

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("🚀 正在启动 depth-Research-Agent 服务...")
    print("👉 Swagger UI 接口文档地址: http://127.0.0.1:8000/docs")
    print("=" * 50 + "\n")

    # 使用 uvicorn 启动服务，开启 reload 方便后续修改代码热更新
    # 暂时把 reload 改为 False 测试一下
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)