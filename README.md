# 🔬 DepthResearch-Agent (深度研究智能体引擎)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B)
![LangGraph](https://img.shields.io/badge/LangGraph-Multi_Agent-orange)
![DeepSeek](https://img.shields.io/badge/LLM-DeepSeek-black)
![Kimi](https://img.shields.io/badge/Parser-Kimi_API-purple)

**DepthResearch-Agent** 是一个基于 `LangGraph` 构建的解耦式、可插拔的多智能体学术研究底座。

本次系统迎来了全面架构升级：深度融合了 **Kimi 高精度文档解析** 与 **DeepSeek 强逻辑推理**，并引入了全新的**智能语义路由**与**多线程提纯**机制。系统能够自主调度主管(Supervisor)、规划(Planner)、检索(Researcher)、评审(Reviewer)与撰写(Writer)智能体，为您提供端到端的沉浸式深度研究体验。

---

## ✨ 核心亮点与技术升级

- 🧠 **智能 HyDE 语义路由 (New)**：底层检索器具备防误触机制。对于极短查询或特定算法术语（如纯英文缩写），自动走快速通道；面对复杂长句提问，则实时调用大模型生成“假设性学术回答”，跨越语义鸿沟。
- ⚡ **多线程并发 LLM 提纯 (New)**：在召回高分文档后，系统利用 `ThreadPoolExecutor` 并发调用大模型，对多段长文本进行“精读”与关键证据压缩，极大降低上下文冗余并提升响应速度。
- 🚀 **开箱即用的本地化网络优化**：内置 `HF_ENDPOINT` 国内高速通道镜像，并使用 `ModelScope` 自动拉取极轻量级 Embedding 模型（BGE-small）。修复了底层 C++ 库 (`KMP_DUPLICATE_LIB_OK`) 冲突问题，告别环境闪退。
- 🔍 **RRF 双引擎混合检索**：底层采用 `FAISS` 稠密语义检索与 `BM25` 稀疏词频检索进行多路召回，通过 RRF (Reciprocal Rank Fusion) 算法精准融合打分，兼顾长尾语义与高频术语。
- 🛡️ **LangGraph 多智能体协同**：独立的 `Peer_Reviewer` 节点强制进行逻辑自洽审查，`Supervisor` 节点根据状态机动态路由工作流，确保最终报告的事实准确性与逻辑严密性。
- 🔌 **沉浸式流式心跳前端**：前后端完全分离。Streamlit 前台接入 FastAPI 流式接口，实时打印各 Agent 节点的工作心跳状态（规划拆解、资料挖掘、同行核查等），工作流全透明。

---

## 📂 项目架构

```text
depth_research_agent/
├── app/                        
│   ├── api/                    # FastAPI 接口层定义 (支持流式传输 Stream)
│   ├── core/                   # 状态机结构 (ResearchState) 定义
│   ├── agents/                 # LangGraph 工作流图 (graph.py) 与 Worker 节点
│   └── rag/                    # OmniRetriever (智能路由/并发提纯/RRF融合) 与 Kimi 解析器
├── data/                       # 本地知识库数据流 (自动管理，Git忽略)
│   ├── raw_docs/               # 用户上传的 PDF 文献库
│   ├── raw_docs_parsed/        # Kimi 智能解析产出的 Markdown 文件
│   └── vector_db/              # FAISS 索引、BM25 词典与 ByteStore 缓存
├── main.py                     # FastAPI 后端引擎启动入口
├── ui.py                       # 沉浸式 Streamlit 前端交互与文献管理器
└── requirements.txt            # 项目核心依赖包
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
