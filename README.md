# 🔬 DepthResearch-Agent (深度研究智能体引擎)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent-orange)
![DeepSeek](https://img.shields.io/badge/LLM-DeepSeek-black)
![Kimi](https://img.shields.io/badge/Parser-Kimi_API-purple)


**DepthResearch-Agent** 是一个基于 `LangGraph` 构建的解耦式、可插拔的多智能体学术研究底座。

当前系统已全面升级，不仅支持一键动态挂载本地 PDF 文献库，更接入了**全网联邦检索**能力。通过融合 Kimi 高精度解析与 DeepSeek 强推理能力，自动完成复杂学术问题的自动领域嗅探、意图拆解、**HyDE 语义增强检索**、多线程并发提纯、**全网旁路救援**与深度报告生成。

---

## ✨ 核心亮点与架构优势 (全新升级)

- ⚡ **多线程并发 LLM 提纯**：在底层检索器中引入多线程机制，并发调用大模型对召回的长文本进行“精读”与关键证据压缩。
- 💡 **HyDE 假设性文档增强 (New)**：在触发底层 RAG 检索前，系统会实时调用大模型生成堆叠了专业术语、指标与算法概念的“假设性学术回答”，以此跨越自然语言提问与专业文献之间的语义鸿沟，极大提升向量匹配精度。
- 🌐 **全网增量检索与旁路救援 (New)**：LangGraph 工作流新增 `External_Search` 节点。当 `Peer_Reviewer` 节点审查发现本地文献证据无法支撑结论时，将自动打回重审并提取新线索，触发大网模型进行全网增量检索，突破本地知识边界。
- 🔍 **RRF 双引擎混合检索**：底层采用 `FAISS` 语义检索与 `BM25` 关键词检索进行多路召回，并运用 RRF (Reciprocal Rank Fusion) 算法进行融合打分，兼顾长尾语义与高频术语。
- 🛡️ **抗幻觉同行评审**：独立的 `Peer_Reviewer` 节点强制进行逻辑自洽审查与交叉验证，确保最终生成的报告具有高度的事实准确性。
- 🔌 **沉浸式流式监控前端**：前后端分离架构全面升级交互体验，Streamlit 前台接入流式 API，实时打印工作流心跳状态（如意图拆解、底层检索、审查反馈等），流程全透明。

---

## 📂 项目架构

```text
depth_research_agent/
├── app/                        
│   ├── api/                    # FastAPI 接口层路由定义
│   ├── core/                   # 状态机结构 (AgentState) 与核心 Prompt 库
│   ├── agents/                 # LangGraph 工作流节点 (Nodes) 与包含外网搜索路由的边 (Edges)
│   └── rag/                    # 包含 HyDE 增强与 RRF 融合的 OmniRetriever，以及 Kimi PDF解析器
├── data/                       # 本地知识库数据流 (Git忽略)
│   ├── raw_docs/               # 用户上传的原始 PDF 文献存放处
│   ├── raw_docs_parsed/        # Kimi 解析产出的标准化 Markdown 文件
│   └── vector_db/              # FAISS 向量索引与 BM25 缓存结构
├── main.py                     # FastAPI 后端引擎启动入口
├── ui.py                       # 支持流式心跳与文献管理的 Streamlit 前台
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
