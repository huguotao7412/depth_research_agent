# app/agents/workers/researcher.py
import os
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.tools import StructuredTool  # 🚨 新增这个导入
from langgraph.prebuilt import create_react_agent
from app.core.state import ResearchState
from app.rag.retrievers import OmniRetriever

# 🔌 引入你写好的 MCP 客户端
from protocols.mcp.client import get_mcp_tools_and_client


async def researcher_node(state: ResearchState) -> dict:
    # 🚨 注意：这里变成了 async def，因为加载 MCP 工具需要 await
    print("\n⏳ [Researcher] 开始工作 (已激活 本地RAG + MCP联邦检索 模式)...")

    api_base = os.getenv("OPENAI_API_BASE", "https://api.deepseek.com/v1")
    llm = ChatOpenAI(
        model="deepseek-chat",
        temperature=0,
        base_url=api_base,
        timeout=60,
        max_retries=2
    )

    instruction = state.get("current_instruction")
    task_desc = instruction.task_description if instruction else "检索相关文献并提取关键数据"

    raw_path = state.get("raw_docs_path", "data/raw_docs")
    db_path = state.get("vector_db_path", "data/vector_db/faiss_index")

    # ==========================================
    # 🛠️ 注册工具 1：本地 RAG 检索工具
    # ==========================================
    @tool
    def search_local_papers(query: str) -> str:
        """
        必须优先调用的工具！用于检索用户本地挂载的 PDF 学术文献数据库。
        输入你想查询的具体关键词或研究问题，返回高相关的文献片段。
        """
        print(f"   [Tool] 📚 正在检索本地知识库: {query[:20]}...")
        retriever = OmniRetriever(raw_docs_path=raw_path, vector_db_path=db_path)
        docs = retriever.retrieve(query)
        if not docs:
            return "【系统返回】: 本地文献库中未找到相关资料。请尝试使用外部网络搜索工具。"
        return "\n\n".join([doc.page_content for doc in docs])

    # ==========================================
    # 🛠️ 注册工具 2：MCP 外部工具 (Tavily & GitHub)
    # ==========================================
    print("   [MCP] 正在初始化并连接外部 MCP 服务器 (Tavily/GitHub)...")
    try:
        mcp_client, raw_mcp_tools = await get_mcp_tools_and_client()

        mcp_tools = []
        for t in raw_mcp_tools:
            # 使用闭包隔离每个工具的作用域
            def make_safe_wrappers(orig_tool):
                def sync_wrapper(**kwargs):
                    try:
                        res = orig_tool.invoke(kwargs)
                        # 如果是列表，提取出里面的 text 字段并用换行符拼接成纯字符串
                        if isinstance(res, list):
                            return "\n".join([str(x.get("text", x)) if isinstance(x, dict) else str(x) for x in res])
                        return str(res)
                    except Exception as e:
                        return f"工具调用异常: {str(e)}"

                async def async_wrapper(**kwargs):
                    try:
                        res = await orig_tool.ainvoke(kwargs)
                        if isinstance(res, list):
                            return "\n".join([str(x.get("text", x)) if isinstance(x, dict) else str(x) for x in res])
                        return str(res)
                    except Exception as e:
                        return f"工具调用异常: {str(e)}"

                return sync_wrapper, async_wrapper

            # 生成安全的同步和异步调用函数
            s_wrap, a_wrap = make_safe_wrappers(t)

            # 重新打包为一个安全的工具
            safe_tool = StructuredTool(
                name=t.name,
                description=t.description,
                args_schema=t.args_schema,
                func=s_wrap,
                coroutine=a_wrap
            )
            mcp_tools.append(safe_tool)

        print(f"   [MCP] ✅ 成功挂载并包装 {len(mcp_tools)} 个防崩溃外部能力！")
    except Exception as e:
        print(f"   [MCP] ⚠️ MCP 初始化失败: {str(e)}。本次任务降级为仅本地。")
        mcp_tools = []

    # 组合所有工具（将本地工具放在最前面）
    tools = [search_local_papers] + mcp_tools

    # ==========================================
    # 🧠 构建具备工具调用能力的子智能体
    # ==========================================
    system_prompt = (
        "你是一个严谨的学术研究员 (Researcher)。"
        "你的任务是根据主管的指令，全面收集学术数据和事实证据。\n\n"
        "⚠️ 【强制执行策略】\n"
        "1. 你必须首先使用 `search_local_papers` 工具查询本地文献库。\n"
        "2. 如果本地库信息不足，或者你需要检索最新的互联网动态、开源仓库代码，你必须自主调用 Tavily 搜索工具或 Github 工具进行补充。\n"
        "3. 完成所有检索后，综合所有获取到的证据，整理出一份翔实的数据卡片或文献摘要。\n"
        "4. 在最终的摘要中，必须客观陈述事实，不要编造任何未检索到的数据。"
    )

    # 创建带有工具的智能体
    research_agent = create_react_agent(llm, tools)

    print("🧠 [Researcher] 正在自主规划检索策略并调用工具 (这可能包含全网搜索，请耐心等待)...")
    try:
        # 我们把系统指令直接作为对话的第一句话塞进去！效果完全等价！
        agent_result = await research_agent.ainvoke({
            "messages": [
                ("system", system_prompt),  # <--- 动态注入你的强制执行策略
                ("user", task_desc)  # <--- 主管派发的具体任务
            ]
        })

        final_content = agent_result["messages"][-1].content
        print("✅ [Researcher] 证据收集完毕！")

    except Exception as e:
        print(f"\n❌ [Researcher] 执行期间发生严重错误或超时: {str(e)}")
        final_content = f"执行过程中发生错误: {str(e)}。无法提供完整的检索数据。"

    # 将新提取的信息存入状态
    new_data = {
        "task": task_desc,
        "extracted_info": final_content
    }
    existing_data = state.get("collected_data") or []

    return {
        "messages": [AIMessage(content=f"【资料收集完毕】\n{final_content}", name="Researcher")],
        "collected_data": existing_data + [new_data]
    }