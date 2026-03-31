# protocols/mcp/client.py
import os
from langchain_mcp_adapters.client import MultiServerMCPClient


def _get_mcp_server_params() -> dict:
    """内部方法：统一管理所有 MCP Server 的配置参数"""
    return {
        "tavily": {
            "command": "npx",
            "args": ["-y", "tavily-mcp@latest"],
            "env": {"TAVILY_API_KEY": os.getenv("TAVILY_API_KEY", "")},
            "transport": "stdio"  # 【修复点】：显式指定通信方式为 stdio
        },
        "github": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_TOKEN", "")},
            "transport": "stdio"  # 【修复点】：显式指定通信方式为 stdio

        }
    }

async def get_mcp_tools_and_client():
    """
    外部接口：初始化并返回 MultiServerMCPClient 实例及其解析出的工具列表。
    """
    params = _get_mcp_server_params()
    client = MultiServerMCPClient(params)
    tools = await client.get_tools()

    return client, tools