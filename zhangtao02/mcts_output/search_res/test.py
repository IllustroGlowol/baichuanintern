import json
import pandas as pd

# 设置输入路径（请替换为你本地文件路径）
input_file = "/data_train/code/mllm/zhangtao02/mcts_output/search_res/7b_test_post0.jsonl"

# 设置输出 Excel 路径
output_excel = "/data_train/code/mllm/zhangtao02/mcts_output/search_res/7braw_jsonl_data.xlsx"

# 提取 Prm_response 字段
records = []
with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        try:
            item = json.loads(line.strip())
            prm = item.get("Prm_response", None)
            if prm:
                records.append([prm])  # 保持为单列 DataFrame
        except Exception as e:
            print(f"❌ 跳过异常数据：{e}")

# 写入 Excel
df = pd.DataFrame(records, columns=["Prm_response"])
df.to_excel(output_excel, index=False)
print(f"✅ 已保存为 Excel 文件：{output_excel}")
