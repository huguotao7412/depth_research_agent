# protocols/mcp/client.py
import os
from langchain_mcp_adapters.client import MultiServerMCPClient
from contextlib import asynccontextmanager

# 全局变量，用于存储已激活的工具和客户端
_GLOBAL_MCP_TOOLS = None
_GLOBAL_MCP_CLIENT = None


def _get_mcp_server_params() -> dict:
    return {
        "tavily": {
            "command": "npx",
            "args": ["-y", "tavily-mcp@latest"],
            "env": {"TAVILY_API_KEY": os.getenv("TAVILY_API_KEY", "")},
            "transport": "stdio"
        },
        "github": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_TOKEN", "")},
            "transport": "stdio"
        }
    }


@asynccontextmanager
async def mcp_lifecycle_manager():
    """
    异步上下文管理器：统一管理 MCP 客户端的物理连接生命周期。
    """
    global _GLOBAL_MCP_CLIENT, _GLOBAL_MCP_TOOLS
    params = _get_mcp_server_params()

    print("🔌 [MCP] 正在通过标准输入输出 (stdio) 拉起 Node.js 子进程...")
    async with MultiServerMCPClient(params) as client:
        _GLOBAL_MCP_CLIENT = client
        _GLOBAL_MCP_TOOLS = await client.get_tools()
        print(f"✅ [MCP] 成功挂载 {len(_GLOBAL_MCP_TOOLS)} 个工具。")
        yield client, _GLOBAL_MCP_TOOLS

    # 离开 context 时，子进程会被自动清理
    _GLOBAL_MCP_CLIENT = None
    _GLOBAL_MCP_TOOLS = None
    print("🛑 [MCP] 已安全关闭所有外部服务器子进程。")


async def get_mcp_tools_and_client():
    """
    业务调用接口：获取全局单例
    """
    if _GLOBAL_MCP_CLIENT is None:
        raise RuntimeError("MCP 客户端尚未初始化，请确保已在 lifespan 中启动。")
    return _GLOBAL_MCP_CLIENT, _GLOBAL_MCP_TOOLS