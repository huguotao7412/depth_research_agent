# 🔬 DepthResearch-Agent (深度研究智能体引擎)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent-orange)

**DepthResearch-Agent** 是一个基于 `LangGraph` 构建的解耦式、可插拔的多智能体协作底座。系统核心逻辑与特定业务领域完全解耦，支持一键动态挂载本地 PDF 文献库。通过接入 **Kimi 大模型高精度解析**与 **DeepSeek 强推理能力**，自动完成学术问题的**意图拆解**、**多路召回检索**、**交叉验证 (抗幻觉)** 与 **深度研究报告生成**。

## ✨ 核心亮点

- ☁️ **云端大模型解析**：摒弃沉重的本地解析库，接入 Kimi (Moonshot) API，将结构复杂的学术 PDF 极速转换为高还原度的 Markdown 格式。
- 🧠 **Agentic RAG 工作流**：基于 LangGraph 构建标准化学术研究 SOP（自动领域嗅探 -> 意图拆解 -> 检索 -> 同行评审 -> 不合格重试 -> 组装报告）。
- 🔍 **双引擎混合检索**：底层使用 `FAISS` (语义向量搜索, 基于 BGE 模型) + `BM25` (高频学术术语检索) 进行多路召回，并使用 RRF 算法进行融合。
- 🛡️ **严格的抗幻觉机制**：独立的 `Peer_Reviewer` 节点强制要求大模型交叉比对召回上下文，若证据不足将打回并触发 `Adaptive_Retriever` 重新检索。
- 🔌 **前后端分离设计**：计算逻辑与交互 UI 完全分离，Streamlit 前端可无缝对接 FastAPI 强大的并发处理能力。

## 📂 项目架构

```text
depth_research_agent/
├── app/                        
│   ├── api/                    # FastAPI 接口层
│   ├── core/                   # 状态机定义 (State) 与动态 Prompt
│   ├── agents/                 # LangGraph 核心工作流节点与路由逻辑
│   └── rag/                    # Kimi 解析器与 FAISS+BM25 混合检索器
├── data/                       # 本地知识库 (Git忽略)
│   ├── parsed_docs/            # Kimi 解析出的 Markdown 文件
│   ├── raw_docs/               # 上传的原始 PDF 文献存放处
│   └── vector_db/              # 向量缓存 (上传/删除文献会自动清理重建)
├── main.py                     # FastAPI 后端启动入口
├── ui.py                       # Streamlit 极简前端界面
└── requirements.txt            # 项目依赖
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