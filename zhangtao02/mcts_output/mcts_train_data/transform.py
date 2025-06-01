import json

# 输入输出路径
input_path = "/data_train/code/mllm/zhangtao02/mcts_output/mcts_train_data/mcts_0414.jsonl"
output_path = "/data_train/code/mllm/zcl/llamafactory/data/mcts_0414_transformed.jsonl"
# 读取输入文件并处理
with open(input_path, "r", encoding="utf-8") as fin, open(output_path, "w", encoding="utf-8") as fout:
    for line in fin:
        item = json.loads(line.strip())

        # 获取问题内容（第一个 path_nodes）
        question_content = item["path_nodes"][0][1]

        # 获取学生步骤内容（拼接其余 path_nodes 的内容）
        student_steps = "\n\n".join([x[1] for x in item["path_nodes"][1:]])

        # 构造 messages 格式
        messages = [
            {
                "role": "user",
                "content": question_content
            },
            {
                "role": "assistant",
                "content": student_steps
            }
        ]

        # 构造最终结构
        new_item = {
            "messages": messages,
            "images": item.get("image", [])
        }

        # 写入
        fout.write(json.dumps(new_item, ensure_ascii=False) + "\n")

print(f"✅ 转换完成，保存至 {output_path}")
