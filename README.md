# 🔬 DepthResearch-Agent (深度研究智能体引擎)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent-orange)

**OmniResearch-Agent** 是一个基于 `LangGraph` 构建的解耦式、可插拔的多智能体协作底座。系统核心逻辑与特定业务领域完全解耦，支持一键动态挂载本地 PDF 文献库，自动完成学术问题的**意图拆解**、**多路召回检索**、**交叉验证 (抗幻觉)** 与 **深度研究报告生成**。

## ✨ 核心亮点

- 🧠 **Agentic RAG 工作流**：基于 LangGraph 构建标准化学术研究 SOP（加载领域 -> 意图拆解 -> 检索 -> 同行评审 -> 不合格重试 -> 组装报告）。
- 🔍 **双引擎混合检索**：底层使用 `FAISS` (语义向量搜索, 基于 BGE 模型) + `BM25` (高频学术术语检索) 进行多路召回，并使用 RRF 算法进行融合。
- 🛡️ **严格的抗幻觉机制**：独立的 `Peer_Reviewer` 节点强制要求大模型交叉比对召回上下文，若证据不足将打回并触发 `Adaptive_Retriever` 重新检索。
- 🔌 **完全解耦设计**：知识库、计算逻辑、前端 UI、后端 API 完全分离。只需在前端拖拽新的 PDF，即可研究全新领域。

## 📂 项目架构

```text
depth_research_agent/
├── app/                        
│   ├── api/                    # FastAPI 接口层
│   ├── core/                   # 状态机定义 (State) 与动态 Prompt
│   ├── agents/                 # LangGraph 核心节点与路由逻辑
│   └── rag/                    # FAISS + BM25 混合检索器
├── data/                       # 本地知识库 (Git忽略)
│   ├── raw_docs/               # PDF 文献存放处
│   └── vector_db/              # 向量索引缓存
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
# 创建并激活虚拟环境 (Windows)
python -m venv .venv
.venv\Scripts\activate

# 安装全部所需依赖
pip install -r requirements.txt