# 🔬 DepthResearch-Agent | 准工业级多智能体深度研究引擎

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![LangGraph](https://img.shields.io/badge/LangGraph-Multi_Agent-FF9900?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-Streaming-009688?style=for-the-badge&logo=fastapi)
![FAISS](https://img.shields.io/badge/Memory-FAISS%20%2B%20BM25-009688?style=for-the-badge)

> **打破“单次对话”的桎梏，构建真实的虚拟学术团队。**
> 全新升级的 **DepthResearch-Agent** 不仅是一个 RAG 工具，更是一个具备**物理隔离沙盒**、**长短期双重记忆**、**领域自动嗅探**的自我进化型科研工作站。

---

## 🔥 架构巨变：本次核心升级亮点

我们对底层引擎进行了脱胎换骨的重构，解决了传统大模型应用中“记忆串味”、“长逻辑崩溃”与“无法量化评估”的三大痛点：

* 🗂️ **多工作区沙盒与静默领域嗅探 (Domain Sniffer)**
    告别知识库大杂烩！系统支持无限创建**物理隔离**的研究区。当你上传该领域的第一篇 PDF 时，后台的 Domain Sniffer 会自动抽取摘要，通过轻量级大模型为你**自动命名该研究领域**（如“毫米波雷达生理监测”），实现极致优雅的知识管理。
* 🧠 **长短期心智双引擎 (Memory Engine)**
    引入全新的 `MemoryManager` 节点，彻底重构记忆机制：
    * **短期防爆**：利用滑动窗口与模型异步摘要，彻底释放 Token，防止深远对话上下文撑爆内存。
    * **长期偏好**：后台静默解析你对 Agent 提出的批评与要求，自动提炼并写入 FAISS 隐式经验库与 JSON 画像。你的每一次纠正，都会让下一次的 `Writer` 节点更加懂你。
* 🚀 **多脑协同与防无限循环 (Actor Cluster)**
    主管 (`Supervisor`) 动态进行快慢系统路由。对于复杂指令，由规划师 (`Planner`) 拆解任务，分发给多个 `Researcher`（Actor）**并发执行**混合检索（本地 RAG + 全网 MCP）。我们为 Actor 引入了强硬的递归退出机制，彻底杜绝了工具调用的死循环。
* 📊 **Ragas 量化体检报告 (Golden Dataset Evaluation)**
    新增独立的量化评测管道 `evaluate_ragas.py`，支持导入黄金测试集，对 Agent 的**上下文精度 (Context Precision)**、**事实忠诚度 (Faithfulness)** 与 **答案相关性 (Answer Relevance)** 进行多维度机打分，让引擎的每一次迭代都有据可依。
* ⚡ **极速响应：DailyQA 快系统**
    面对简单名词解释（如“什么是 ICA 算法”），系统会自动短路复杂的规划和审查流程，直接唤醒低延迟模型极速响应。

---

## 🛠 硬核技术栈 (Tech Stack)

- **核心编排:** `LangGraph` (包含内置 `MemorySaver` 状态机)
- **多模型基座:** 强推理模型 `DeepSeek` + 高性价比极速模型 `GLM-4-Flash`
- **解析与存储:** `Kimi API` (异步复杂版面还原) + `FAISS` & `Rank-BM25` (多向量混合召回) + `BGE-M3` (Rerank 重排序)
- **外部扩展:** 基于 `Model Context Protocol (MCP)` 挂载 Tavily 联邦检索引擎
- **交互与通信:** `FastAPI` (原生异步处理与 SSE 流式心跳) + `Streamlit` (极简多沙盒驾驶舱)

---

## 📂 项目结构全景

```text
depth_research_agent/
├── app/                        
│   ├── api/                    # FastAPI 核心接口与工作区路由
│   ├── core/                   # 状态机 (ResearchState) / LLM 工厂 / Memory Store (长短期记忆)
│   ├── agents/                 # 多智能体节点 (Supervisor/Planner/Actor/Reviewer/Writer/Memory)
│   └── rag/                    # Kimi 异步解析器与 OmniRetriever 混合检索引擎
├── data/                       # 📂 多工作区物理隔离库 (自动生成)
│   ├── workspace_1/            # 独立研究沙盒 1
│   │   ├── raw_docs/           # PDF 原文库
│   │   ├── vector_db/          # FAISS / BM25 独立索引
│   │   └── memory/             # JSON画像与避坑经验FAISS库
│   └── workspaces.json         # 全局域注册表 (由 Sniffer 自动更新)
├── protocols/                  # Agent 协议层与 MCP 客户端
├── evaluate_ragas.py           # 📊 Ragas 量化评测引擎
├── main.py                     # API 后端点火开关
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
