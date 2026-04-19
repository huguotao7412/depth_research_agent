# evaluate_ragas.py
import os
import asyncio
import pandas as pd
from datasets import Dataset

# 引入 Ragas 评测指标
from ragas import evaluate
from ragas.metrics import (
    context_precision,  # 上下文精度 (检索到的文献是否真的是回答问题所需要的)
    faithfulness,  # 忠实度/反幻觉率 (Writer 的报告是否全基于检索数据，没有瞎编)
    answer_relevance  # 答案相关性 (报告有没有完美解答用户的初始问题)
)
# 针对部分模型需要包装
from langchain_openai import ChatOpenAI

# 引入您的核心业务代码
from langchain_core.messages import HumanMessage
from app.agents.graph import build_multi_agent_graph
from app.core.llm_factory import get_llm, get_embeddings


async def run_evaluation():
    print("🚀 启动 Ragas 量化评测管道...")

    # ==========================================
    # 1. 定义黄金测试集 (Golden Dataset)
    # 建议您替换为毫米波雷达/您具体领域的真实问题和人工标准答案
    # ==========================================
    eval_questions = [
        "毫米波雷达在非接触式心率监测中，通常使用什么算法来消除呼吸带来的相位干扰？",
        "什么是独立成分分析(ICA)，它在雷达信号处理中的主要作用是什么？"
    ]

    ground_truths = [
        "通常使用正交解调提取相位，并结合带通滤波或经验模态分解(EMD)等算法来分离和消除呼吸引起的低频高幅相位干扰。",
        "独立成分分析(ICA)是一种盲源分离技术。在雷达信号处理中，主要用于从混合的反射信号中，将相互独立的心跳信号和呼吸信号分离开来。"
    ]

    # ==========================================
    # 2. 初始化您的深度研究引擎
    # ==========================================
    # 注意：这里我们使用大模型作为“评测裁判”。为了节约成本，直接复用您配好的模型。
    main_llm = get_llm(model_type="main", temperature=0.0)
    embeddings = get_embeddings()

    # 实例化您的 Agent Graph
    research_agent = build_multi_agent_graph(main_llm)

    answers = []
    contexts_list = []

    # ==========================================
    # 3. 模拟执行并收集状态 (Execution)
    # ==========================================
    for idx, q in enumerate(eval_questions):
        print(f"\n🧪 正在测试第 {idx + 1}/{len(eval_questions)} 题: {q}")

        # 模拟前端传入的入参 (使用一个专门的评测工作区)
        inputs = {
            "messages": [HumanMessage(content=q)],
            "workspace_id": "eval_workspace",
            "raw_docs_path": "data/eval_workspace/raw_docs",
            "vector_db_path": "data/eval_workspace/vector_db/faiss_index"
        }
        config = {"configurable": {"thread_id": f"eval_thread_{idx}"}, "recursion_limit": 50}

        try:
            # 执行图流转
            final_state = await research_agent.ainvoke(inputs, config=config)

            # 从您的状态机中提取最终报告
            final_report = final_state.get("final_draft", "")
            answers.append(final_report)

            # 🚨 核心映射：将 Researcher 并发收集到的证据，转化为 Ragas 要求的 contexts 格式
            collected_data = final_state.get("collected_data", [])
            retrieved_contexts = [data.get("extracted_info", "") for data in collected_data if
                                  data.get("extracted_info")]

            # 如果没查到数据，给个空字符串兜底
            if not retrieved_contexts:
                retrieved_contexts = ["未检索到任何背景信息"]

            contexts_list.append(retrieved_contexts)
            print(f"   ✅ 完成！生成了 {len(final_report)} 字报告，使用了 {len(retrieved_contexts)} 段证据。")

        except Exception as e:
            print(f"   ❌ 执行崩溃: {e}")
            answers.append("执行失败")
            contexts_list.append(["执行失败"])

    # ==========================================
    # 4. 构建 HuggingFace Dataset 并开始 Ragas 评测
    # ==========================================
    data = {
        "question": eval_questions,
        "answer": answers,
        "contexts": contexts_list,
        "ground_truth": ground_truths
    }
    dataset = Dataset.from_dict(data)

    print("\n⚖️ 正在召唤 LLM 裁判进行多维度量化打分 (请耐心等待)...")

    # 运行 Ragas 评测
    result = evaluate(
        dataset=dataset,
        metrics=[
            context_precision,
            faithfulness,
            answer_relevance
        ],
        llm=main_llm,
        embeddings=embeddings
    )

    # ==========================================
    # 5. 输出量化体检报告
    # ==========================================
    df = result.to_pandas()
    print("\n📊 =============== 深度研究智能体评测报告 ===============")
    print(f"整体得分概览:\n{result}")
    print("========================================================\n")

    # 将详细数据保存为 CSV 供后续分析
    df.to_csv("ragas_evaluation_report.csv", index=False, encoding="utf-8-sig")
    print("📁 详细每题得分已保存至: ragas_evaluation_report.csv")


if __name__ == "__main__":
    asyncio.run(run_evaluation())