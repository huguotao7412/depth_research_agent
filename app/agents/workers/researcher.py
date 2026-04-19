# app/agents/workers/researcher.py
import os
import asyncio
from langchain_core.messages import AIMessage
from langchain_core.tools import tool
from langchain_core.tools import StructuredTool
from langgraph.prebuilt import create_react_agent
from app.core.state import ResearchState

# 🔌 引入你写好的 MCP 客户端
from protocols.mcp.client import get_mcp_tools_and_client
from app.core.llm_factory import get_llm
from app.rag.retrievers import get_retriever


async def researcher_node(state: ResearchState) -> dict:
    print("\n⏳ [Actor Cluster] 接收到分解任务，正在唤醒多 Actor 并行计算引擎...")

    llm = get_llm(model_type="main", temperature=0.0)

    instruction = state.get("current_instruction")
    task_desc = instruction.task_description if instruction else "检索相关文献并提取关键数据"

    raw_path = state.get("raw_docs_path", "data/raw_docs")
    db_path = state.get("vector_db_path", "data/vector_db/faiss_index")

    # ==========================================
    # 🛠️ 注册工具 1：本地 RAG 检索工具
    # ==========================================
    local_retriever = get_retriever(raw_docs_path=raw_path, vector_db_path=db_path)

    @tool
    async def search_local_papers(query: str) -> str:
        """
        必须优先调用的工具！用于检索用户本地挂载的 PDF 学术文献数据库。
        输入你想查询的具体关键词或研究问题，返回高相关的文献片段。
        """
        print(f"   [Tool] 📚 正在检索本地知识库: {query[:20]}...")
        docs = await local_retriever.aretrieve(query)
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
                        return parse_mcp_result(orig_tool.invoke(kwargs))
                    except Exception as e:
                        return f"工具调用异常: {str(e)}"

                async def async_wrapper(**kwargs):
                    try:
                        return parse_mcp_result(await orig_tool.ainvoke(kwargs))
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
    # 🧠 构建具备工具调用能力的子智能体 (Actor)
    # ==========================================
    system_prompt = (
        "你是一个极其专注的学术执行体 (Actor)。"
        "你的任务是只针对当前分配给你的【特定子任务】，调用工具全面收集证据。\n\n"
        "⚠️ 【强制执行策略与引用规范 - 必须严格遵守】\n"
        "1. 你必须首先使用 `search_local_papers` 工具查询本地文献库。\n"
        "2. 如果信息不足，必须自主调用 Tavily 搜索工具等进行补充。\n"
        "3. 【至关重要】：在综合整理获取到的证据时，你必须把每一条核心信息所对应的【来源】清晰地标注在该条信息的末尾。\n"
        "   - 对于本地文献：请标注 `(来源: xxx.pdf)`\n"
        "   - 对于网络搜索：请**必须直接使用** Markdown 超链接语法，格式为 `[参考网页](完整的URL)`，绝不能在总结中暴露纯文本长链接。\n"
        "4. 在最终输出的摘要中，必须客观陈述事实，不要编造任何未检索到的数据和来源链接。\n"
        "5. 🛑 【防死循环指令】：最多连续调用工具不超过 5 次。一旦收集到足够支撑任务的核心信息，必须立刻停止检索，直接输出最终的文字总结报告，绝不能无休止地反复调用工具！"
    )

    # ==========================================
    # ⚡ 核心改造：并行执行逻辑 (Concurrency Optimization)
    # ==========================================
    # 🚨 关键修复：判断是否为 Reviewer 打回重做阶段
    messages = state.get("messages", [])
    has_been_reviewed = any(msg.name == "Reviewer" for msg in messages)

    if has_been_reviewed:
        print("⚠️ [Actor Cluster] 检测到 Reviewer 审查打回，进入【精准补充检索】模式...")
        # 补充检索模式下，不再执行 Planner 的全量大纲，而是直接执行 Supervisor 针对性下发的补充指令
        tasks = [task_desc]
    else:
        # 初次执行，走 Planner 拆解的并发大纲
        tasks = state.get("research_plan", [])
        if not tasks:
            tasks = [task_desc]

    # 定义单个 Actor 的运行生命周期
    async def run_single_actor(single_task_desc: str, index: int):
        print(f"   🚀 [Actor-{index}] 认领并启动子任务: {single_task_desc[:30]}...")

        # 每次都单独实例化 Agent，确保各自的状态和工具调用历史完全隔离
        actor_agent = create_react_agent(llm, tools)

        try:
            agent_result = await actor_agent.ainvoke({
                "messages": [
                    ("system", system_prompt),
                    ("user", f"请完成以下数据收集任务：\n{single_task_desc}")
                ]
            }, config={"recursion_limit": 15})

            final_content = agent_result["messages"][-1].content
            print(f"   ✅ [Actor-{index}] 任务圆满完成！")

            return {
                "task": single_task_desc,
                "extracted_info": final_content,
                "source": "详见上方内容中提取的【来源文献/网页】标注"
            }
        except Exception as e:
            print(f"   ❌ [Actor-{index}] 执行期间发生异常或超时: {str(e)}")
            return {
                "task": single_task_desc,
                "extracted_info": f"执行失败: {str(e)}。无法提供完整的检索数据。",
                "source": "无"
            }

    # 使用 asyncio.gather 拉起多个独立任务并发请求
    print(f"🧠 [Actor Cluster] 正在同时拉起 {len(tasks)} 个 Actor 智能体并行工作...")

    collected_results = await asyncio.gather(
        *(run_single_actor(task, i + 1) for i, task in enumerate(tasks))
    )

    print("✅ [Actor Cluster] 所有并行任务证据收集完毕！")

    return {
        "messages": [AIMessage(content=f"【Actor Cluster 汇报】\n成功并发执行 {len(tasks)} 个检索子任务，资料收集完毕。",
                               name="Researcher")],
        "collected_data": collected_results
    }