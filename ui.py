import streamlit as st
import os
import requests
import json
import time

# --- 全局 API 与路径配置 ---
API_BASE_URL = "http://127.0.0.1:8000/api/v1"
STREAM_API_URL = f"{API_BASE_URL}/research/stream"
# 仅用于前端展示列表（读权限），写权限已全部移交后端 API
DOCS_DIR = os.path.join("data", "raw_docs")

# 确保前端读取目录存在（防报错）
os.makedirs(DOCS_DIR, exist_ok=True)

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
st.caption("您的解耦式、可插拔通用深度研究智能体引擎 (支持全网联邦检索)")
st.divider()

# ==========================================
# 侧边栏：干净整洁的文献库管理 (API 解耦版)
# ==========================================
with st.sidebar:
    st.header("📚 本地知识核心")
    st.markdown("上传或管理您的专属 PDF 学术文献。")

    # 1. 丝滑上传文件组件
    uploaded_files = st.file_uploader(
        "➕ 挂载新文献",
        type=["pdf"],
        accept_multiple_files=True,
        help="上传新的 PDF，系统将通过后端 API 自动异步解析建库。"
    )

    if uploaded_files:
        with st.spinner("正在安全传输至后端并启动建库..."):
            for file in uploaded_files:
                files = {"file": (file.name, file.getvalue(), "application/pdf")}
                try:
                    # 🚨 替换旧版操作：呼叫 FastAPI 的 Upload 接口
                    requests.post(f"{API_BASE_URL}/docs/upload", files=files)
                except Exception as e:
                    st.error(f"传输失败: {e}")

        # ✅ 使用 Toast 替代 success，防止页面重载时闪烁，体验极佳
        st.toast("✅ 成功挂载文献！后台正在建立索引。")
        time.sleep(0.6)  # 短暂延迟，让视觉停留
        st.rerun()

    st.divider()

    # 2. 已有文献列表与对齐修复
    st.subheader("当前已挂载文献")
    current_files = [f for f in os.listdir(DOCS_DIR) if f.endswith(".pdf")] if os.path.exists(DOCS_DIR) else []

    if not current_files:
        st.info("文献库当前为空。")
    else:
        with st.expander(f"查看文献目录 (共 {len(current_files)} 篇)", expanded=True):
            for file in current_files:
                col1, col2 = st.columns([0.85, 0.15], vertical_alignment="center")
                display_name = file if len(file) < 26 else file[:23] + "..."
                col1.markdown(f"<div class='file-name-text'>📄 {display_name}</div>", unsafe_allow_html=True)

                if col2.button("🗑️", key=f"del_{file}", help=f"删除 {file}"):
                    try:
                        # 🚨 替换旧版操作：呼叫 FastAPI 的 Delete 接口
                        requests.delete(f"{API_BASE_URL}/docs/{file}")
                        st.toast(f"🗑️ 已移除 {file} 并触发缓存清理！")
                        time.sleep(0.6)
                        st.rerun()
                    except Exception as e:
                        st.error(f"删除失败: {str(e)}")


# ==========================================
# 辅助函数：绘制高颜值 Agent 流水线
# ==========================================
def render_pipeline_html(active_node: str) -> str:
    nodes = ["Planner", "Researcher", "Writer", "Reviewer"]
    items = []
    for n in nodes:
        if n == active_node:
            # 激活节点：高亮色 + 粗体
            items.append(f"<span style='color: #009688; font-weight: bold;'>🟢 {n}</span>")
        else:
            # 未激活节点：置灰
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
                "chat_history": st.session_state.chat_history[:-1]  # 传给后端历史记录
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
                                pipeline_placeholder.empty()  # 完成后隐藏流水线图
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

                                # 1. 动态更新流水线可视化图
                                if node in ["Planner", "Researcher", "Writer", "Reviewer"]:
                                    pipeline_placeholder.markdown(render_pipeline_html(node), unsafe_allow_html=True)

                                # 2. 差异化高亮日志输出，拒绝杂乱无章
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
                                        f"🔍 **[Researcher]** 正在混合双擎 (本地 RAG + 全网 MCP) 挖掘核心证据...")
                                elif node == "Reviewer":
                                    log_container.error(f"⚖️ **[Reviewer]** 启动严苛审查，核对逻辑严密性与事实出处...")
                                elif node == "Writer":
                                    log_container.markdown(f"> 📝 **[Writer]** 正在汇总所有事实数据，奋笔疾书...")
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

        # 状态流转结束后，将大模型最终产出的学术报告进行优雅渲染
        if final_report:
            st.markdown(final_report)

            # 🚨 核心 Bug 修复：记录最新说话的 Agent 是 Writer，保证历史对话连通性
            st.session_state.chat_history.append({
                "role": "assistant",
                "name": "Writer",
                "content": final_report
            })