# app/agents/workers/researcher.py
import os
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.tools import StructuredTool
from langgraph.prebuilt import create_react_agent
from app.core.state import ResearchState
from app.rag.retrievers import OmniRetriever

# 🔌 引入你写好的 MCP 客户端
from protocols.mcp.client import get_mcp_tools_and_client
from app.core.llm_factory import get_llm


async def researcher_node(state: ResearchState) -> dict:
    print("\n⏳ [Researcher] 开始工作 (已激活 本地RAG + MCP联邦检索 模式)...")

    llm = get_llm(model_type="main", temperature=0.0)

    instruction = state.get("current_instruction")
    task_desc = instruction.task_description if instruction else "检索相关文献并提取关键数据"

    raw_path = state.get("raw_docs_path", "data/raw_docs")
    db_path = state.get("vector_db_path", "data/vector_db/faiss_index")

    # ==========================================
    # 🛠️ 注册工具 1：本地 RAG 检索工具 (✅ 新增提取来源 metadata)
    # ==========================================
    @tool
    async def search_local_papers(query: str) -> str:
        """
        必须优先调用的工具！用于检索用户本地挂载的 PDF 学术文献数据库。
        输入你想查询的具体关键词或研究问题，返回高相关的文献片段。
        """
        print(f"   [Tool] 📚 正在检索本地知识库: {query[:20]}...")
        retriever = OmniRetriever(raw_docs_path=raw_path, vector_db_path=db_path)
        docs =await retriever.aretrieve(query)
        if not docs:
            return "【系统返回】: 本地文献库中未找到相关资料。请尝试使用外部网络搜索工具。"

        # 将文档内容和文件名来源拼接到一起，让大模型知道这是来自哪篇文献
        results = []
        for doc in docs:
            source = doc.metadata.get("source", "未知本地文档")
            filename = os.path.basename(source)  # 仅提取文件名部分以保持整洁
            results.append(f"【来源文献: {filename}】\n{doc.page_content}")

        return "\n\n".join(results)

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

                # 内部通用解析逻辑：提取文本和 URL 来源
                def parse_mcp_result(res):
                    if isinstance(res, list):
                        parsed_items = []
                        for x in res:
                            if isinstance(x, dict):
                                content = x.get("content", x.get("text", str(x)))
                                url = x.get("url", "")
                                # 如果有URL来源，则拼接到返回内容中
                                if url:
                                    parsed_items.append(f"来源：[参考网页]({url})\n{content}")
                                else:
                                    parsed_items.append(str(content))
                            else:
                                parsed_items.append(str(x))
                        return "\n".join(parsed_items)
                    return str(res)

                def sync_wrapper(**kwargs):
                    try:
                        res = orig_tool.invoke(kwargs)
                        return parse_mcp_result(res)
                    except Exception as e:
                        return f"工具调用异常: {str(e)}"

                async def async_wrapper(**kwargs):
                    try:
                        res = await orig_tool.ainvoke(kwargs)
                        return parse_mcp_result(res)
                    except Exception as e:
                        return f"工具调用异常: {str(e)}"

                return sync_wrapper, async_wrapper

            s_wrap, a_wrap = make_safe_wrappers(t)

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

    tools = [search_local_papers] + mcp_tools

    # ==========================================
    # 🧠 构建具备工具调用能力的子智能体 (✅ 强化引用标注提示词)
    # ==========================================
    system_prompt = (
        "你是一个严谨的学术研究员 (Researcher)。"
        "你的任务是根据主管的指令，全面收集学术数据和事实证据。\n\n"
        "⚠️ 【强制执行策略与引用规范 - 必须严格遵守】\n"
        "1. 你必须首先使用 `search_local_papers` 工具查询本地文献库。\n"
        "2. 如果信息不足，必须自主调用 Tavily 搜索工具等进行补充。\n"
        "3. 【至关重要】：在综合整理获取到的证据时，你必须把每一条核心信息所对应的【来源】清晰地标注在该条信息的末尾。\n"
        "   - 对于本地文献：请标注 `(来源: xxx.pdf)`\n"
        "   - 对于网络搜索：请**必须直接使用** Markdown 超链接语法，格式为 `[参考网页](完整的URL)`，绝不能在总结中暴露纯文本长链接。\n"
        "4. 在最终输出的摘要中，必须客观陈述事实，不要编造任何未检索到的数据和来源链接。"
    )

    research_agent = create_react_agent(llm, tools)

    print("🧠 [Researcher] 正在自主规划检索策略并调用工具 (这可能包含全网搜索，请耐心等待)...")
    try:
        agent_result = await research_agent.ainvoke({
            "messages": [
                ("system", system_prompt),
                ("user", task_desc)
            ]
        })

        final_content = agent_result["messages"][-1].content
        print("✅ [Researcher] 证据收集完毕！")

    except Exception as e:
        print(f"\n❌ [Researcher] 执行期间发生严重错误或超时: {str(e)}")
        final_content = f"执行过程中发生错误: {str(e)}。无法提供完整的检索数据。"

    # ✅ 这里增加一个通用的 source 字段，并让 Writer 注意 final_content 里自带的来源标注
    new_data = {
        "task": task_desc,
        "extracted_info": final_content,
        "source": "详见上方内容中提取的【来源文献/网页】标注"
    }
    existing_data = state.get("collected_data") or []

    return {
        "messages": [AIMessage(content=f"【资料收集完毕】\n{final_content}", name="Researcher")],
        "collected_data": existing_data + [new_data]
    }