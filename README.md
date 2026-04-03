# 🔬 DepthResearch-Agent | 下一代多智能体深度研究引擎

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![LangGraph](https://img.shields.io/badge/LangGraph-Multi_Agent-FF9900?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-Streaming-009688?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-Immersive_UI-FF4B4B?style=for-the-badge&logo=streamlit)
![DeepSeek](https://img.shields.io/badge/LLM-DeepSeek-black?style=for-the-badge)
![Kimi](https://img.shields.io/badge/Parser-Kimi_API-purple?style=for-the-badge)

> **还在为堆积如山的 PDF 文献和漫无目的的全网检索发愁吗？**
> 欢迎来到自动化科研的新纪元。**DepthResearch-Agent** 彻底重塑了学术研究与深度调研的工作流。我们不仅提供了一个工具，更为您配备了一支**不知疲倦、严谨苛刻的虚拟学术团队**。

---

## 🔥 核心优势 (Why Choose Us?)

传统的大模型应用往往受限于“单脑思考”和“数据幻觉”。DepthResearch-Agent 通过极致的架构设计，为您带来降维打击般的体验：

* 🧠 **多脑协同，复刻真实学术团队**
    系统内置五大独立智能体：**主管(Supervisor)**全局调度、**规划师(Planner)**庖丁解牛、**研究员(Researcher)**深度挖掘、**审查员(Reviewer)**严苛把关、**撰稿人(Writer)**落笔生花。各司其职，自我纠错，拒绝“大模型一本正经地胡说八道”。
* 📡 **本地+全网 混合双擎检索 (RAG + MCP)**
    本地资料匮乏？不用担心。我们在双路高精度本地召回（FAISS + BM25）的基础上，无缝挂载 **MCP 联邦检索**（Tavily/GitHub）。一旦本地文献不足，Agent 会自动突破边界，进行全网实时追踪。
* 🎯 **极致无损，PDF 变身“结构化富矿”**
    抛弃粗糙的开源解析方案。我们深度集成 **Kimi 高精度文档解析**，完美还原复杂学术 PDF 中的表格、多级标题与段落，搭配 BGE-M3 向量模型，确保每一个关键数据都不被遗漏。
* 🛡️ **零幻觉，字字皆有出处的“铁律”**
    生成的每一条核心结论，都必须携带清晰的来源标注（精准到具体 PDF 文件名或可点击的网页超链接）。没有证据，绝不编造！
* ⚡ **全景透明，流式心跳交互 (SSE)**
    拒绝“黑盒等待”。基于 FastAPI + Streamlit 打造的前后分离架构，实时打印各大智能体的工作心跳与思考轨迹，让您像大 Boss 一样沉浸式看着您的虚拟团队为您冲锋陷阵。

---

## 🛠 硬核技术栈 (Tech Stack)

本项目采用目前最前沿的 AI 应用开发组合：

- **智能体编排 (Orchestration):** `LangGraph` (基于状态机的循环调度与容错机制)
- **大模型基座 (LLM Core):** 强推理模型 `DeepSeek` (主节点) + 高性价比模型 `GLM-4-Flash` (规划/提纯节点)
- **文档解析 (Document Parsing):** `Kimi (Moonshot) API` (长文本/复杂版面异步提取)
- **混合检索 (Hybrid Retrieval):** `FAISS` (密集向量) + `Rank-BM25` (稀疏词频) + `SiliconFlow BGE-M3` (Rerank 重排序)
- **外部拓展 (Tooling):** `Model Context Protocol (MCP)` 挂载 Tavily 等全网搜索引擎
- **高性能后端 (Backend):** `FastAPI` (原生异步处理与 SSE 流式推送)
- **交互层 (Frontend):** `Streamlit` (极简、专注的交互体验)

---

## 📂 优雅的架构设计

```text
depth_research_agent/
├── app/                        
│   ├── api/                    # FastAPI 核心接口 (支持 SSE 流式心跳)
│   ├── core/                   # 全局状态机 (ResearchState) 与 LLM 工厂
│   ├── agents/                 # LangGraph 多智能体工作流引擎 (Supervisor等5大节点)
│   └── rag/                    # OmniRetriever (并发提纯/RRF融合) 与 Kimi 解析器
├── data/                       # 您的专属知识保险箱 (本地化隔离)
│   ├── raw_docs/               # PDF 原文库
│   ├── raw_docs_parsed/        # 结构化 Markdown 数据
│   └── vector_db/              # 向量、词典与键值对缓存
├── protocols/                  # A2A (Agent to Agent) 通信协议与 MCP 外部接口
├── main.py                     # API 引擎点火开关
└── ui.py                       # Streamlit 沉浸式驾驶舱
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
# 【必填】主力大模型配置 (默认推荐 DeepSeek)
MAIN_LLM_BASE_URL="[https://api.deepseek.com/v1](https://api.deepseek.com/v1)"
MAIN_LLM_API_KEY="your_deepseek_api_key"
MAIN_LLM_MODEL_NAME="deepseek-chat"

# 【必填】轻量模型配置 (用于大纲规划与数据提纯，推荐 GLM-4)
FAST_LLM_BASE_URL="[https://open.bigmodel.cn/api/paas/v4/](https://open.bigmodel.cn/api/paas/v4/)"
FAST_LLM_API_KEY="your_zhipu_api_key"
FAST_LLM_MODEL_NAME="glm-4-flash"

# 【必填】文献解析与向量化 (Kimi + SiliconFlow)
MOONSHOT_API_KEY="your_kimi_api_key"
EMBEDDING_BASE_URL="[https://api.siliconflow.cn/v1](https://api.siliconflow.cn/v1)"
EMBEDDING_API_KEY="your_siliconflow_api_key"
EMBEDDING_MODEL_NAME="BAAI/bge-m3"

# 【可选】MCP 全网搜索配置
TAVILY_API_KEY="your_tavily_api_key"
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
