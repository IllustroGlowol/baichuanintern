# import requests
# headers = {"Authorization": f"Bearer {API_TOKEN}"}
# API_URL = "https://huggingface.co/api/datasets/ibm/duorc/croissant"
# def query():
#     response = requests.get(API_URL, headers=headers)
#     return response.json()
# data = query()
import json
import re
from collections import defaultdict

# 设置文件路径（你可以替换成自己的本地路径）
file_path = "/global_data/mllm/zcl/llamafactory/llamafactory/data/sciprm0430_fixed.jsonl"

# 初始化学科统计表
subject_count = defaultdict(int)

# 学科关键词（按优先顺序）
subjects = ["math", "geography", "biology", "chemistry", "physics"]

# 逐行读取并统计
with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        images = data.get("images", [])
        matched = False
        for img_path in images:
            for subject in subjects:
                if subject in img_path.lower():
                    subject_count[subject] += 1
                    matched = True
                    break  # 每个样本只记一次
            if matched:
                break

# 打印统计结果
print("Subject-wise Sample Count:")
for subject in subjects:
    print(f"{subject}: {subject_count[subject]}")
