import json

# 文件路径
file_path = "/data_train/code/mllm/zcl/llamafactory/data/math_mcts_0424.jsonl"

def clean_and_patch_images(record):
    # 删除所有 <image> 标签
    for msg in record.get("messages", []):
        if "content" in msg:
            msg["content"] = msg["content"].replace("<image>", "")

    # 根据 images 数量添加对应数量的 <image> 到 messages[0]
    num_images = len(record.get("images", []))
    if num_images > 0 and len(record["messages"]) > 0:
        record["messages"][0]["content"] = record["messages"][0]["content"].rstrip() + "\n" + "<image>\n" * num_images
        record["messages"][0]["content"] = record["messages"][0]["content"].strip()

    return record

# 读取、处理、覆盖写回
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

with open(file_path, "w", encoding="utf-8") as f:
    for line in lines:
        record = json.loads(line.strip())
        record = clean_and_patch_images(record)
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

print(f"✅ 已在原文件中完成清洗和 <image> 标签补全：{file_path}")