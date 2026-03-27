# 🔬 DepthResearch-Agent (深度研究智能体引擎)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent-orange)
![DeepSeek](https://img.shields.io/badge/LLM-DeepSeek-black)
![Kimi](https://img.shields.io/badge/Parser-Kimi_API-purple)

**DepthResearch-Agent** 是一个基于 `LangGraph` 构建的解耦式、可插拔的多智能体学术研究底座。

系统核心逻辑与特定业务领域完全解耦，支持一键动态挂载本地 PDF 文献库。通过接入 **Kimi 大模型高精度解析**与 **DeepSeek 强推理能力**，自动完成复杂学术问题的**自动领域嗅探**、**意图拆解**、**双引擎混合检索**、**多线程 LLM 动态并发提纯**、**交叉验证 (抗幻觉)** 与 **深度研究报告生成**。

---

## ✨ 核心亮点与架构优势

- ⚡ **多线程并发 LLM 提纯 (New)**：在底层检索器中引入多线程机制，并发调用大模型对召回的长文本进行“精读”与关键证据压缩。彻底过滤噪音，极大节省后续节点的 Token 消耗并成倍降低响应延迟。
- ☁️ **云端大模型极速解析**：摒弃沉重的本地 OCR/PDF 解析库，原生接入 Kimi (Moonshot) API，将结构复杂、包含图表的学术 PDF 极速转换为高还原度的 Markdown 格式。
- 🧠 **Agentic RAG 标准工作流**：基于 LangGraph 构建了严谨的学术研究 SOP：`自动领域嗅探 -> 意图拆解 -> 动态检索与提纯 -> 同行评审 -> (不合格重试) -> 组装报告`。
- 🔍 **双引擎混合检索 (RRF融合)**：底层采用 `FAISS` (语义向量搜索, 基于 BGE 模型) + `BM25` (高频学术术语检索) 进行多路召回。深度优化了 FAISS 的底层序列化逻辑，确保超高稳定性的本地 K-V 映射读取。
- 🛡️ **严格的抗幻觉防御机制**：独立的 `Peer_Reviewer` 节点强制要求大模型交叉比对召回的上下文，若检测到“证据不足”将直接打回，并触发 `Adaptive_Retriever` 重新进行更深度的检索。
- 🔌 **前后端分离架构**：计算逻辑与交互 UI 完全分离，FastAPI 提供强大的高并发异步接口，Streamlit 提供极简直观的交互前台。

---

## 📂 项目架构

```text
depth_research_agent/
├── app/                        
│   ├── api/                    # FastAPI 接口层路由定义
│   ├── core/                   # 状态机结构 (AgentState) 与核心 Prompt 库
│   ├── agents/                 # LangGraph 工作流节点 (Nodes) 与路由边 (Edges)
│   └── rag/                    # OmniRetriever (混合检索/并发提纯) 与 Kimi PDF解析器
├── data/                       # 本地知识库数据流 (Git忽略)
│   ├── raw_docs/               # 用户上传的原始 PDF 文献存放处
│   ├── raw_docs_parsed/        # Kimi 解析产出的标准化 Markdown 文件
│   └── vector_db/              # FAISS 向量索引与 BM25 缓存结构
├── main.py                     # FastAPI 后端引擎启动入口
├── ui.py                       # Streamlit 极简前台交互界面
└── requirements.txt            # 项目轻量化核心依赖
```
## 🚀 快速启动 (Quick Start)

只需简单几步，即可在本地部署并体验您的专属深度研究智能体。

### 1. 克隆项目与安装依赖
首先，将代码克隆到本地并进入项目目录：
```bash
git clone [https://github.com/huguotao7412/depth_research_agent](https://github.com/huguotao7412/depth_research_agent)
cd depth_research_agent

# 创建并激活虚拟环境
python -m venv .venv
source .venv/bin/activate  # Windows 用户使用: .venv\Scripts\activate

# 安装轻量化核心依赖
pip install -r requirements.txt
```
### 2. 环境配置 (.env)
在项目根目录下创建一个 .env 文件，并填入以下内容。本项目默认使用 DeepSeek 进行逻辑推理，Kimi (Moonshot) 进行 PDF 解析：
```bash
# Kimi (Moonshot) API Key - 用于云端高精度 PDF 解析
MOONSHOT_API_KEY="sk-你的Kimi密钥"

# DeepSeek API 配置 - 用于 LangGraph 逻辑推理与报告生成
OPENAI_API_BASE="[https://api.deepseek.com/v1](https://api.deepseek.com/v1)"
OPENAI_API_KEY="sk-你的DeepSeek密钥"
```
### 3. 启动系统
本项目采用前后端分离设计，需要分别启动后端 API 服务和前端 UI 服务。
启动后端 API 服务：
```bash
python main.py
# 引擎将在 [http://127.0.0.1:8000](http://127.0.0.1:8000) 启动，可访问 /docs 查看 API 文档
```
启动前端 UI 服务：
```bash
streamlit run ui.py
# 浏览器将自动打开交互界面，支持上传 PDF 文献并提交研究问题
```
