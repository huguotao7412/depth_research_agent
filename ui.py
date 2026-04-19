# ui.py
import streamlit as st
import os
import requests
import json
import time

# --- 全局 API 与路径配置 ---
API_BASE_URL = "http://127.0.0.1:8000/api/v1"
STREAM_API_URL = f"{API_BASE_URL}/research/stream"

# --- 页面基础配置 ---
st.set_page_config(
    page_title="Depth Research Agent",
    page_icon="🔬",
    layout="wide",  # 宽屏模式
    initial_sidebar_state="expanded"
)

# --- 全局 CSS 深度美化 ---
st.markdown("""
<style>
    /* 隐藏默认的部署和菜单按钮 */
    .stDeployButton {display:none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* 调整聊天气泡字体，增强学术阅读体验 */
    .st-emotion-cache-1c7y2kd p, .st-emotion-cache-zt5idj p {
        font-family: 'Inter', "Source Sans Pro", "PingFang SC", sans-serif;
        font-size: 1.05rem;
        line-height: 1.6;
    }

    /* 修复侧边栏文件列表的对齐问题：移除按钮自带的冗余边距 */
    .stButton > button {
        padding: 0px 8px !important;
        margin-top: 0px !important;
        min-height: 32px !important;
        border: none;
        background-color: transparent;
    }
    .stButton > button:hover {
        background-color: #ff4b4b20;
        border-radius: 4px;
    }

    /* 调整 Markdown 容器底部边距，使其与按钮水平居中 */
    .file-name-text {
        margin-bottom: 0px;
        padding-top: 4px;
        font-size: 0.9rem;
        color: #e0e0e0;
    }

    /* 自定义工作流状态栏 UI */
    .pipeline-container {
        background-color: #f8f9fa;
        padding: 12px 15px;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        margin-bottom: 15px;
        font-family: monospace;
        font-size: 14px;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# --- 界面标题区域 ---
st.title("🔬 Depth Research Agent")
st.caption("您的解耦式、可插拔通用深度研究智能体引擎 (多工作区隔离版本)")
st.divider()

# ==========================================
# 获取与配置工作区映射表 (Domain Registry)
# ==========================================
try:
    # 动态拉取注册表，防止本地未预热
    workspaces = requests.get(f"{API_BASE_URL}/workspaces").json()
except Exception:
    workspaces = {"workspace_1": {"display_name": "系统尚未就绪，请检查后端"}}

ws_ids = list(workspaces.keys())


def format_ws(ws_id):
    # 下拉菜单显示 AI 嗅探后的高大上名称
    return workspaces[ws_id].get("display_name", ws_id)


with st.sidebar:
    st.header("🗂️ 领域隔离区")

    # 🚨 核心：选择工作区
    selected_ws = st.selectbox("当前活跃研究区", options=ws_ids, format_func=format_ws)

    # 🚨 核心：新建工作区
    if st.button("➕ 建立新研究区", use_container_width=True):
        res = requests.post(f"{API_BASE_URL}/workspaces").json()
        st.session_state.current_ws = res["workspace_id"]
        st.session_state.chat_history = [
            {"role": "assistant", "name": "System",
             "content": "✨ 全新物理隔离区创建成功！\n\n请在左侧上传该领域的首篇文献，我将在后台默默分析并为您正式命名该领域。"}
        ]
        st.rerun()

    # 监控工作区切换，无缝清空上一个领域的上下文记忆，防止串味
    if "current_ws" not in st.session_state:
        st.session_state.current_ws = selected_ws

    if st.session_state.current_ws != selected_ws:
        st.session_state.current_ws = selected_ws
        st.session_state.chat_history = [
            {"role": "assistant", "name": "System",
             "content": f"✅ 已无缝切换至：**{format_ws(selected_ws)}**。\n\n当前处于物理隔离的沙盒环境，请输入您的研究问题。"}
        ]
        st.rerun()

    st.divider()
    st.header("📚 本领域专属文献")
    st.markdown("上传或管理当前隔离区的文献。")

    # 🚨 动态匹配当前工作区的物理目录
    DOCS_DIR = os.path.join("data", selected_ws, "raw_docs")
    os.makedirs(DOCS_DIR, exist_ok=True)

    # 1. 丝滑上传文件组件
    uploaded_files = st.file_uploader(
        "➕ 挂载新文献",
        type=["pdf"],
        accept_multiple_files=True,
        help="上传新的 PDF，系统将自动划分到当前沙盒区。"
    )

    if uploaded_files:
        with st.spinner("正在传输并启动后台静默分析..."):
            for file in uploaded_files:
                files = {"file": (file.name, file.getvalue(), "application/pdf")}
                try:
                    # 🚨 附带工作区 ID 调用
                    requests.post(f"{API_BASE_URL}/docs/upload", files=files, data={"workspace_id": selected_ws})
                except Exception as e:
                    st.error(f"传输失败: {e}")

        st.toast("✅ 文献就绪！后台嗅探与建库已开启。")
        time.sleep(0.6)
        st.rerun()

    # 2. 已有文献列表与对齐修复
    st.subheader("已挂载文献 (当前区)")
    current_files = [f for f in os.listdir(DOCS_DIR) if f.endswith(".pdf")] if os.path.exists(DOCS_DIR) else []

    if not current_files:
        st.info("当前研究区暂无文献。")
    else:
        with st.expander(f"查看文献目录 (共 {len(current_files)} 篇)", expanded=True):
            for file in current_files:
                col1, col2 = st.columns([0.85, 0.15], vertical_alignment="center")
                display_name = file if len(file) < 26 else file[:23] + "..."
                col1.markdown(f"<div class='file-name-text'>📄 {display_name}</div>", unsafe_allow_html=True)

                if col2.button("🗑️", key=f"del_{file}", help=f"删除 {file}"):
                    try:
                        # 🚨 附带工作区 ID 调用删除
                        requests.delete(f"{API_BASE_URL}/docs/{file}", params={"workspace_id": selected_ws})
                        st.toast(f"🗑️ 已移除 {file} 并触发缓存清理！")
                        time.sleep(0.6)
                        st.rerun()
                    except Exception as e:
                        st.error(f"删除失败: {str(e)}")


# ==========================================
# 辅助函数：绘制高颜值 Agent 流水线
# ==========================================
def render_pipeline_html(active_node: str) -> str:
    if active_node == "DailyQA":
        return "<div class='pipeline-container'>⚡ <b>动态路由 (快系统):</b> &nbsp;&nbsp; <span style='color: #FF9900; font-weight: bold;'>🟢 极速问答引擎 (DailyQA)</span> ➔ 结束</div>"
    nodes = ["Planner", "Researcher", "Writer", "Reviewer"]
    items = []
    for n in nodes:
        if n == active_node:
            items.append(f"<span style='color: #009688; font-weight: bold;'>🟢 {n}</span>")
        else:
            items.append(f"<span style='color: #adb5bd;'>⚪ {n}</span>")

    pipeline_str = " ➔ ".join(items)
    return f"<div class='pipeline-container'>🌊 <b>多智能体流转:</b> &nbsp;&nbsp; {pipeline_str}</div>"


# ==========================================
# 主体区域：沉浸式聊天交互界面
# ==========================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "name": "System",
         "content": "您好！我是 **Depth Research Agent**。我已经准备好在您的本地文献和广阔的互联网中寻找答案了。请输入您的研究问题。"}
    ]

# 渲染历史对话
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=True)

# 接收用户输入问题
if user_input := st.chat_input("在此输入您的研究问题"):

    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.status("🧠 引擎点火中，正在初始化 Agent 团队...", expanded=True) as status_box:

            # 布局占位符：上方显示动态流水线，下方显示详细日志
            pipeline_placeholder = st.empty()
            log_container = st.container()

            # 初始化流水线显示
            pipeline_placeholder.markdown(render_pipeline_html("Supervisor"), unsafe_allow_html=True)

            payload = {
                "query": user_input,
                "workspace_id": selected_ws,  # 🚨 附带工作区 ID 驱动全局计算流转
                "chat_history": st.session_state.chat_history[:-1]
            }

            final_report = ""
            start_time = time.time()

            try:
                response = requests.post(STREAM_API_URL, json=payload, stream=True)
                response.raise_for_status()

                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8')
                        if decoded_line.startswith("data: "):
                            data_str = decoded_line[6:]

                            if data_str == "[DONE]":
                                end_time = time.time()
                                pipeline_placeholder.empty()
                                status_box.update(label=f"✅ 深度研究完成！总耗时: {end_time - start_time:.1f}s",
                                                  state="complete", expanded=False)
                                break

                            try:
                                event = json.loads(data_str)
                                if "error" in event:
                                    st.error(f"❌ 后端执行异常: {event['error']}")
                                    status_box.update(label="任务中断", state="error")
                                    break

                                node = event.get("node")
                                state = event.get("state_update", {})

                                if node in ["Planner", "Researcher", "Writer", "Reviewer", "DailyQA"]:
                                    pipeline_placeholder.markdown(render_pipeline_html(node), unsafe_allow_html=True)

                                if node == "Supervisor":
                                    next_agent = state.get("next", "未知")
                                    if next_agent != "FINISH":
                                        log_container.info(
                                            f"👔 **[Supervisor]** 审视全局，下一步任务分发 ➔ **{next_agent}**")
                                elif node == "Planner":
                                    plan = state.get("research_plan", [])
                                    log_container.success(
                                        f"🗓️ **[Planner]** 庖丁解牛，已规划出 {len(plan)} 个独立研究步骤。")
                                elif node == "Researcher":
                                    log_container.warning(
                                        f"🔍 **[Actor Cluster]** 正在混合双擎 (本地 RAG + 全网 MCP) 并发挖掘证据...")
                                elif node == "Reviewer":
                                    log_container.error(f"⚖️ **[Reviewer]** 启动严苛审查，核对逻辑严密性与事实出处...")
                                elif node == "Writer":
                                    log_container.markdown(f"> 📝 **[Writer]** 正在汇总所有事实数据，奋笔疾书...")
                                    final_report = state.get("final_draft", "")
                                elif node == "DailyQA":
                                    log_container.success(f"⚡ **[DailyQA]** 成功短路复杂流程，正在通过快模型极速回复...")
                                    final_report = state.get("final_draft", "")

                            except json.JSONDecodeError:
                                continue

            except requests.exceptions.ConnectionError:
                error_msg = "⚠️ **无法连接到后端引擎！** 请检查 `main.py` 是否已启动并在监听 8000 端口。"
                status_box.update(label="网络异常", state="error")
                st.error(error_msg)
            except Exception as e:
                status_box.update(label="系统异常", state="error")
                st.error(f"发生未知错误: {str(e)}")

        if final_report:
            st.markdown(final_report)
            st.session_state.chat_history.append({
                "role": "assistant",
                "name": "Writer",
                "content": final_report
            })