import os
import sys
from dotenv import load_dotenv
load_dotenv()

# 将项目根目录加入 sys.path，确保能正确导入 app 模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.agents.graph import build_omni_research_graph


def test_workflow():
    # 1. 加载环境变量 (请确保根目录有 .env 文件并配置了 OPENAI_API_KEY)


    if not os.environ.get("OPENAI_API_KEY") and not os.environ.get("OPENAI_BASE_URL"):
        print("⚠️ 警告: 未检测到大模型 API 环境变量。请在 .env 中配置，否则 Query_Analyzer 和 Peer_Reviewer 会报错。")

    print("🚀 初始化 OmniResearch-Agent 图结构...")
    graph = build_omni_research_graph()

    # 2. 构造测试输入
    test_query = "基于毫米波雷达提取脉搏波传导速度(PWV)进行连续血压预测时，主要的信号处理难点与误差来源是什么？"
    inputs = {"query": test_query}

    print(f"\n[{'=' * 50}]")
    print(f"开始执行测试，研究问题: {test_query}")
    print(f"[{'=' * 50}]\n")

    # 3. 使用 stream 观察状态机的每一步流转
    # stream_mode="updates" 会在每次节点执行完毕后，返回对 State 的增量修改
    for output in graph.stream(inputs, stream_mode="updates"):
        for node_name, state_update in output.items():
            print(f"✅ [节点执行完毕]: {node_name}")

            # 打印关键的状态更新信息
            if "domain_config" in state_update:
                print(f"   -> 加载领域: {state_update['domain_config'].get('domain')}")
            if "sub_questions" in state_update:
                print(f"   -> 拆解子问题: {state_update['sub_questions']}")
            if "documents" in state_update:
                print(f"   -> 模拟检索到文献数量: {len(state_update['documents'])} 篇")
            if "review_feedback" in state_update:
                print(f"   -> 评审反馈: {state_update['review_feedback']}")
            if "final_report" in state_update:
                print("\n" + "=" * 50)
                print("🎓 最终深度研究报告生成成功！内容如下：\n")
                print(state_update['final_report'])
                print("=" * 50 + "\n")

            print("-" * 30)

    print("\n🎉 测试流转完成！")


if __name__ == "__main__":
    test_workflow()