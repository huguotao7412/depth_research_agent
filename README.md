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

- **🧠 LangGraph 多智能体协作**：内置 Supervisor（主管）、Planner（规划师）、Researcher（研究员）、Writer（撰稿人）和 Reviewer（审查员），严格遵循学术工作流。
- **📚 混合检索与 RAG 架构**：
  - **本地文献库**：集成 Kimi API 进行 PDF 异步精准解析，使用 SiliconFlow (BGE-M3) 生成向量，结合 FAISS + BM25 实现双路高精度召回。
  - **动态 HyDE 拓展**：对复杂的长句查询自动生成假设性学术回答，增强检索准确度。
- **🌐 MCP 联邦检索**：无缝挂载 Tavily 和 GitHub 等外部工具，本地资料不足时自动进行全网深度搜索。
- **📝 严格的溯源与引用规范**：所有生成的关键结论均会携带明确来源（本地 PDF 文件名或合规的 Markdown 网页超链接），杜绝大模型幻觉。
- **🎨 动态行文风格**：无论是结构严谨的“深度研究报告”，还是自然流畅的“国内外研究现状（文献综述）”，Writer 节点都能根据指令自适应调整排版与行文逻辑。
- **🔌 沉浸式流式心跳前端**：前后端完全分离。Streamlit 前台接入 FastAPI 流式接口，实时打印各 Agent 节点的工作心跳状态（规划拆解、资料挖掘、同行核查等），工作流全透明。

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
# 大模型配置 (默认使用 DeepSeek)
OPENAI_API_BASE="[https://api.deepseek.com/v1](https://api.deepseek.com/v1)"
OPENAI_API_KEY="your_deepseek_api_key"

# Planner 节点使用智谱 GLM-4
ZHIPU_API_KEY="your_zhipu_api_key"

# 文献解析与向量化
MOONSHOT_API_KEY="your_kimi_api_key" # 用于长文本 PDF 解析
EMBEDDING_API_KEY="your_siliconflow_api_key" # 硅基流动 BGE-M3 向量模型
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
