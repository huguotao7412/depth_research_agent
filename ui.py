import streamlit as st
import os
import shutil
import requests
import time

# --- 全局后台配置 (需与 main.py 保持一致) ---
DOCS_DIR = os.path.join("data", "raw_docs")
INDEX_DIR = os.path.join("data", "vector_db", "faiss_index")
# FastAPI 后端接口地址
API_URL = "http://127.0.0.1:8000/api/v1/research"

# 确保文献目录存在
os.makedirs(DOCS_DIR, exist_ok=True)

# --- 页面基础配置 ---
st.set_page_config(
    page_title="depth research agent",
    page_icon="🔬",
    layout="wide",  # 使用宽屏模式，更适合学术阅读
    initial_sidebar_state="expanded"  # 默认展开侧边栏
)

# 全局 CSS 样式微调，让字体更适合阅读，界面更紧凑
# 【已修复】：将 unsafe_allow_warnings 改为 unsafe_allow_html
st.markdown("""
<style>
    .stDeployButton {display:none;} /* 隐藏右上角 deploy 按钮 */
    #MainMenu {visibility: hidden;} /* 隐藏菜单 */
    footer {visibility: hidden;} /* 隐藏页脚 */
    /* 调整聊天气泡的字体 */
    .st-emotion-cache-1c7y2kd p, .st-emotion-cache-zt5idj p {
        font-family: 'Inter', "Source Sans Pro", sans-serif;
        font-size: 1.05rem;
        line-height: 1.6;
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
st.title("🔬 depth research agent")
st.caption("您的解耦式、可插拔通用深度研究智能体引擎")
st.divider()

# --- 侧边栏：简洁版文献库管理 ---
with st.sidebar:
    st.header("📚 本地文献库")
    st.markdown("管理您用于构建知识库的 PDF 学术文献。")

    # 1. 上传文件组件 (支持多文件)
    uploaded_files = st.file_uploader(
        "添加 PDF 文献",
        type=["pdf"],
        accept_multiple_files=True,
        help="上传新的 PDF 论文或报告，系统将自动解析并建立索引。"
    )

    if uploaded_files:
        with st.spinner("正在上传文献并清理旧缓存..."):
            for file in uploaded_files:
                file_path = os.path.join(DOCS_DIR, file.name)
                # 只有文件不存在时才保存，防止重复上传带来的缓存问题
                if not os.path.exists(file_path):
                    with open(file_path, "wb") as f:
                        f.write(file.getbuffer())
            # 上传新文件必须清理向量索引缓存
            clear_index_cache()
        st.success(f"成功上传 {len(uploaded_files)} 篇文献！下一次提问将自动重建索引。")
        time.sleep(1)  # 稍微等待让用户看清提示
        st.rerun()  # 强制刷新界面

    st.divider()

    # 2. 已有文献列表与删除
    st.subheader("当前文献列表")
    current_files = [f for f in os.listdir(DOCS_DIR) if f.endswith(".pdf")]

    if not current_files:
        st.info("文献库当前为空。请上传 PDF 文件以开始。")
    else:
        # 使用 st.expander 将列表收纳，保持侧边栏简洁
        with st.expander(f"查看详情 (共 {len(current_files)} 篇)", expanded=True):
            for file in current_files:
                col1, col2 = st.columns([7, 1])
                # 截断过长的文件名以保持对齐
                display_name = file if len(file) < 30 else file[:27] + "..."
                col1.markdown(f"📄 `{display_name}`")

                # 删除按钮
                if col2.button("🗑️", key=f"del_{file}", help=f"从知识库中移除 {file}"):
                    try:
                        os.remove(os.path.join(DOCS_DIR, file))
                        # 删除文件也必须清理向量索引缓存
                        clear_index_cache()
                        st.warning(f"已移除 {file}")
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        st.error(f"移除文件失败: {str(e)}")

# --- 主体区域：干净的聊天交互界面 ---

# 1. 初始化会话状态 (聊天历史)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant",
         "content": "您好！我是 **depth research agent**。请在左侧文献库中添加研究材料，然后向我提交您的深度研究问题。"}
    ]

# 2. 渲染历史对话 (Markdown 格式)
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        # 【已修复】：将 unsafe_allow_warnings 改为 unsafe_allow_html
        st.markdown(msg["content"], unsafe_allow_html=True)

# 3. 接收用户输入问题
if user_input := st.chat_input("在此输入您的研究问题..."):
    # 显示用户问题
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 4. 呼叫后端 Agent API 并展示动态效果
    with st.chat_message("assistant"):
        # 学术风的 Spinner
        with st.spinner("**depth research agent** 正在为您进行多智能体协作研究... (可能需要几分钟，请耐心等待)"):
            try:
                start_time = time.time()
                # 发送 POST 请求给 FastAPI 后端
                response = requests.post(API_URL, json={"query": user_input}, timeout=None)
                end_time = time.time()

                if response.status_code == 200:
                    data = response.json()

                    # --- 极简输出逻辑 (技术细节折叠) ---
                    sub_questions = data.get("sub_questions", [])
                    docs_count = data.get("retrieved_docs_count", 0)
                    feedback = data.get("feedback_log", "未记录")
                    report_body = data.get("final_report", "报告生成失败。")

                    # 1. 成功召回简报 (第一行)
                    brief_summary = f"✅ 研究完成。耗时: `{end_time - start_time:.1f}s`。参考了本地库中 **{docs_count}** 个高相关性文献片段。"
                    st.markdown(brief_summary)

                    # 2. 将中间所有技术细节折叠起来，保持界面简洁
                    with st.expander("查看 Agent 思考路径与学术评审反馈", expanded=False):
                        st.markdown("**🧠 意图拆解与子问题：**")
                        if sub_questions:
                            for q in sub_questions:
                                st.write(f"- {q}")
                        else:
                            st.write("- (未记录子问题)")

                        st.divider()
                        st.markdown(f"**⚖️ 同行评审反馈信号：**\n`{feedback}`")

                    # 3. 渲染最关键的 Markdown 报告主体
                    st.divider()
                    st.markdown(report_body)

                    # 将完整的简洁版回答存入历史记录
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": f"{brief_summary}\n\n---\n\n{report_body}"
                    })

                else:
                    error_detail = f"**后端 API 报错 (状态码: {response.status_code})**\n\n错误信息: `{response.text}`"
                    st.error(error_detail)
                    st.session_state.chat_history.append({"role": "assistant", "content": error_detail})

            except requests.exceptions.ConnectionError:
                error_msg = "⚠️ **无法连接到后端服务器！** 请确保您的后端引擎 (`main.py`) 已在另一个终端成功启动并运行在 8000 端口。"
                st.error(error_msg)
                st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
            except requests.exceptions.Timeout:
                error_msg = "⏱️ **请求超时。** 您的研究问题可能需要极长时间或本地文献过于庞大。请检查后端状态。"
                st.error(error_msg)
                st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
            except Exception as e:
                error_msg = f"发生未知错误: {str(e)}"
                st.error(error_msg)
                st.session_state.chat_history.append({"role": "assistant", "content": error_msg})