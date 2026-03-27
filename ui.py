import streamlit as st
import os
import shutil
import requests
import json
import time

# --- 全局后台配置 (需与 main.py 保持一致) ---
DOCS_DIR = os.path.join("data", "raw_docs")
INDEX_DIR = os.path.join("data", "vector_db", "faiss_index")
# FastAPI 后端流式接口地址 (请确保与后端的路由设计一致)
STREAM_API_URL = "http://127.0.0.1:8000/api/v1/research/stream"

# 确保文献目录存在
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
</style>
""", unsafe_allow_html=True)


# --- 辅助功能函数 ---
def clear_index_cache():
    """增删文献时清空本地向量索引缓存，强制后端下一次重建"""
    if os.path.exists(INDEX_DIR):
        try:
            shutil.rmtree(INDEX_DIR)
        except Exception as e:
            st.sidebar.error(f"清理索引缓存失败: {str(e)}")


# --- 界面标题区域 ---
st.title("🔬 Depth Research Agent")
st.caption("您的解耦式、可插拔通用深度研究智能体引擎 (支持全网联邦检索)")
st.divider()

# --- 侧边栏：干净整洁的文献库管理 ---
with st.sidebar:
    st.header("📚 本地知识核心")
    st.markdown("上传或管理您的专属 PDF 学术文献。")

    # 1. 上传文件组件
    uploaded_files = st.file_uploader(
        "➕ 挂载新文献",
        type=["pdf"],
        accept_multiple_files=True,
        help="上传新的 PDF 论文或报告，系统将在下一次查询时自动解析建库。"
    )

    if uploaded_files:
        with st.spinner("正在写入硬盘并清理旧索引..."):
            for file in uploaded_files:
                file_path = os.path.join(DOCS_DIR, file.name)
                if not os.path.exists(file_path):
                    with open(file_path, "wb") as f:
                        f.write(file.getbuffer())
            clear_index_cache()
        st.success(f"✅ 成功挂载 {len(uploaded_files)} 篇文献！")
        time.sleep(1)
        st.rerun()

    st.divider()

    # 2. 已有文献列表与对齐修复
    st.subheader("当前已挂载文献")
    current_files = [f for f in os.listdir(DOCS_DIR) if f.endswith(".pdf")]

    if not current_files:
        st.info("文献库当前为空。")
    else:
        with st.expander(f"查看文献目录 (共 {len(current_files)} 篇)", expanded=True):
            for file in current_files:
                # 使用 vertical_alignment 强行让文字和按钮在一条水平线上
                col1, col2 = st.columns([0.85, 0.15], vertical_alignment="center")

                display_name = file if len(file) < 26 else file[:23] + "..."
                col1.markdown(f"<div class='file-name-text'>📄 {display_name}</div>", unsafe_allow_html=True)

                if col2.button("🗑️", key=f"del_{file}", help=f"删除 {file}"):
                    try:
                        os.remove(os.path.join(DOCS_DIR, file))
                        clear_index_cache()
                        st.rerun()
                    except Exception as e:
                        st.error(f"删除失败: {str(e)}")

# --- 主体区域：沉浸式聊天交互界面 ---

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant",
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
        # 使用流式状态盒替代死板的 Spinner
        with st.status("🧠 深度研究智能体已启动，正在规划工作流...", expanded=True) as status_box:

            payload = {"query": user_input}
            final_report = ""
            start_time = time.time()

            try:
                # 开启 stream=True 进行流式接收
                response = requests.post(STREAM_API_URL, json=payload, stream=True)
                response.raise_for_status()

                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8')
                        if decoded_line.startswith("data: "):
                            data_str = decoded_line[6:]

                            if data_str == "[DONE]":
                                end_time = time.time()
                                status_box.update(label=f"✅ 研究完成！总耗时: {end_time - start_time:.1f}s",
                                                  state="complete", expanded=False)
                                break

                            try:
                                event = json.loads(data_str)
                                if "error" in event:
                                    st.error(f"❌ 后端执行出错: {event['error']}")
                                    status_box.update(label="任务失败", state="error")
                                    break

                                node = event.get("node")
                                state = event.get("state_update", {})

                                # ===== 动态更新前端心跳日志 =====
                                if node == "Domain_Configurator":
                                    st.write("✅ **[知识预载]** 领域配置与术语库就绪。")
                                elif node == "Query_Analyzer":
                                    subs = state.get('sub_questions', [])
                                    st.write(f"🔍 **[意图拆解]** 剥离出 {len(subs)} 个子检索策略...")
                                elif node == "Adaptive_Retriever":
                                    docs = state.get("documents", [])
                                    st.write(f"📖 **[底层检索]** 从向量库中萃取了 {len(docs)} 条核心事实证据。")
                                elif node == "Peer_Reviewer":
                                    feedback = state.get("review_feedback", "")
                                    if "APPROVED" in feedback:
                                        st.write("⚖️ **[同行评审]** 证据链路完整，逻辑自洽，审查通过！")
                                    else:
                                        new_q = state.get("search_queries", [])
                                        st.write("⚠️ **[抗幻觉审查]** 发现现有证据无法支撑结论，已打回重审。")
                                        st.write(f"💡 **[自我反思]** 提取新搜索线索: `{', '.join(new_q)}`")
                                elif node == "External_Search":
                                    st.write("🌐 **[突破边界]** 触发旁路救援，正在呼叫大网模型进行全网增量检索...")
                                elif node == "Report_Compiler":
                                    st.write("📝 **[知识融合]** 正在汇总合规证据，撰写最终深度报告...")
                                    final_report = state.get("final_report", "")

                            except json.JSONDecodeError:
                                continue

            except requests.exceptions.ConnectionError:
                error_msg = "⚠️ **无法连接到后端引擎！** 请检查 `main.py` 是否运行在 8000 端口。"
                status_box.update(label="网络异常", state="error")
                st.error(error_msg)
            except Exception as e:
                status_box.update(label="执行异常", state="error")
                st.error(f"发生未知错误: {str(e)}")

        # 状态框结束后，优雅地渲染最终的大模型 Markdown 报告
        if final_report:
            st.markdown(final_report)

            # 持久化保存到聊天记录中
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": final_report
            })