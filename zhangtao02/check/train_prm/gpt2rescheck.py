# import json

# # 定义标准步骤标记列表
# valid_labels = [
#     "步骤正确", "图像认知错误", "题意理解错误",
#     "缺乏相关知识", "知识应用错误", "逻辑过程错误",
#     "幻觉错误", "运算处理错误", "与步骤类型标签无关"
# ]

# # 输入路径
# input_path = "/data_train/code/mllm/zhangtao02/check/train_prm/sci50w_llavacot_error.jsonl"
# # 输出路径
# invalid_output_path = "/data_train/code/mllm/zhangtao02/check/train_prm/sci50w_llavacot_error_invalid.jsonl"
# valid_all_output_path = "/data_train/code/mllm/zhangtao02/check/train_prm/sci50w_llavacot_error_valid.jsonl"
# valid_no_unrelated_output_path = "/data_train/code/mllm/zhangtao02/check/train_prm/sci50w_llavacot_error_valid_no_unrelated.jsonl"
# valid_with_unrelated_output_path = "/data_train/code/mllm/zhangtao02/check/train_prm/sci50w_llavacot_error_valid_with_unrelated.jsonl"

# # 记录
# invalid_samples = []
# valid_samples = []
# valid_samples_with_unrelated = []
# valid_samples_no_unrelated = []

# total_count = 0
# invalid_count = 0
# valid_count = 0

# # 打开并读取
# with open(input_path, "r", encoding="utf-8") as fin:
#     for line in fin:
#         total_count += 1
#         try:
#             sample = json.loads(line.strip())
#         except Exception as e:
#             print(f"⚠️ 第 {total_count} 行 JSON 解析失败，跳过。错误：{e}")
#             continue

#         gpt2res = sample.get("gpt2res", None)

#         # 直接判定非法的情况
#         if not isinstance(gpt2res, list):
#             invalid_samples.append(sample)
#             invalid_count += 1
#             continue

#         # 检查gpt2res中的每个子步骤
#         is_invalid = False
#         has_unrelated = False
#         for idx, step in enumerate(gpt2res):
#             if not isinstance(step, list) or len(step) < 3:
#                 is_invalid = True
#                 break
#             label = step[2]
#             if label not in valid_labels:
#                 is_invalid = True
#                 break
#             if label == "与步骤类型标签无关":
#                 has_unrelated = True
        
#         if is_invalid:
#             invalid_samples.append(sample)
#             invalid_count += 1
#         else:
#             valid_samples.append(sample)
#             valid_count += 1
#             if has_unrelated:
#                 valid_samples_with_unrelated.append(sample)
#             else:
#                 valid_samples_no_unrelated.append(sample)

# # 保存不合格样本
# if invalid_samples:
#     with open(invalid_output_path, "w", encoding="utf-8") as fout:
#         for sample in invalid_samples:
#             fout.write(json.dumps(sample, ensure_ascii=False) + "\n")

# # 保存所有合格样本
# if valid_samples:
#     with open(valid_all_output_path, "w", encoding="utf-8") as fout:
#         for sample in valid_samples:
#             fout.write(json.dumps(sample, ensure_ascii=False) + "\n")

# # 保存合格且无"与步骤类型标签无关"的样本
# if valid_samples_no_unrelated:
#     with open(valid_no_unrelated_output_path, "w", encoding="utf-8") as fout:
#         for sample in valid_samples_no_unrelated:
#             fout.write(json.dumps(sample, ensure_ascii=False) + "\n")

# # 保存合格但包含"与步骤类型标签无关"的样本
# if valid_samples_with_unrelated:
#     with open(valid_with_unrelated_output_path, "w", encoding="utf-8") as fout:
#         for sample in valid_samples_with_unrelated:
#             fout.write(json.dumps(sample, ensure_ascii=False) + "\n")

# # 打印总结
# print(f"🔎 检查完成，总样本数: {total_count}")
# print(f"✅ 合格样本数: {valid_count}")
# print(f"❌ 不合格样本数: {invalid_count}")
# print(f"✅ 合格且无'与步骤类型标签无关'样本数: {len(valid_samples_no_unrelated)}，保存到: {valid_no_unrelated_output_path}")
# print(f"✅ 合格但包含'与步骤类型标签无关'样本数: {len(valid_samples_with_unrelated)}，保存到: {valid_with_unrelated_output_path}")
# print(f"✅ 所有合格样本保存到: {valid_all_output_path}")
# print(f"❌ 不合法样本保存到: {invalid_output_path}")
# import json

# # 标准的步骤标记
# valid_labels = [
#     "步骤正确", "图像认知错误", "题意理解错误",
#     "缺乏相关知识", "知识应用错误", "逻辑过程错误",
#     "幻觉错误", "运算处理错误", "与步骤类型标签无关"
# ]

# # 文件路径
# input_path = "/data_train/code/mllm/zhangtao02/check/train_prm/sci50w_perfect.jsonl"
# invalid_output_path = "/data_train/code/mllm/zhangtao02/check/train_prm/sci50w_perfect_invalid.jsonl"
# valid_all_output_path = "/data_train/code/mllm/zhangtao02/check/train_prm/sci50w_perfect_valid.jsonl"
# valid_no_unrelated_output_path = "/data_train/code/mllm/zhangtao02/check/train_prm/sci50w_perfect_valid_no_unrelated.jsonl"
# valid_with_unrelated_output_path = "/data_train/code/mllm/zhangtao02/check/train_prm/sci50w_perfect_valid_with_unrelated.jsonl"

# # 记录
# invalid_samples = []
# valid_samples = []
# valid_samples_no_unrelated = []
# valid_samples_with_unrelated = []

# total_count = 0
# invalid_count = 0
# valid_count = 0

# # 打开文件开始读取
# with open(input_path, "r", encoding="utf-8") as fin:
#     for line in fin:
#         total_count += 1
#         try:
#             sample = json.loads(line.strip())
#         except Exception as e:
#             print(f"⚠️ 第 {total_count} 行 JSON 解析失败，跳过。错误：{e}")
#             continue

#         gpt2res = sample.get("gpt2res", None)
#         path_nodes = sample.get("path_nodes", None)

#         # 直接非法的情况
#         if not isinstance(gpt2res, list) or not isinstance(path_nodes, list):
#             invalid_samples.append(sample)
#             invalid_count += 1
#             continue

#         # 新增的长度规则校验
#         expected_len = len(path_nodes) - 1
#         if len(gpt2res) != expected_len:
#             invalid_samples.append(sample)
#             invalid_count += 1
#             continue

#         # 检查每个步骤是否合法
#         is_invalid = False
#         has_unrelated = False
#         for idx, step in enumerate(gpt2res):
#             if not isinstance(step, list) or len(step) < 3:
#                 is_invalid = True
#                 break
#             label = step[1]  # 注意！gpt2res这里步骤标记在第2个元素！
#             if label not in valid_labels:
#                 is_invalid = True
#                 break
#             if label == "与步骤类型标签无关":
#                 has_unrelated = True

#         if is_invalid:
#             invalid_samples.append(sample)
#             invalid_count += 1
#         else:
#             valid_samples.append(sample)
#             valid_count += 1
#             if has_unrelated:
#                 valid_samples_with_unrelated.append(sample)
#             else:
#                 valid_samples_no_unrelated.append(sample)

# # 保存不合规样本
# if invalid_samples:
#     with open(invalid_output_path, "w", encoding="utf-8") as fout:
#         for sample in invalid_samples:
#             fout.write(json.dumps(sample, ensure_ascii=False) + "\n")

# # 保存所有合规样本
# if valid_samples:
#     with open(valid_all_output_path, "w", encoding="utf-8") as fout:
#         for sample in valid_samples:
#             fout.write(json.dumps(sample, ensure_ascii=False) + "\n")

# # 保存合规且无"与步骤类型标签无关"的样本
# if valid_samples_no_unrelated:
#     with open(valid_no_unrelated_output_path, "w", encoding="utf-8") as fout:
#         for sample in valid_samples_no_unrelated:
#             fout.write(json.dumps(sample, ensure_ascii=False) + "\n")

# # 保存合规且有"与步骤类型标签无关"的样本
# if valid_samples_with_unrelated:
#     with open(valid_with_unrelated_output_path, "w", encoding="utf-8") as fout:
#         for sample in valid_samples_with_unrelated:
#             fout.write(json.dumps(sample, ensure_ascii=False) + "\n")

# # 打印总结
# print(f"🔎 检查完成，总样本数: {total_count}")
# print(f"✅ 合格样本数: {valid_count}")
# print(f"❌ 不合格样本数: {invalid_count}")
# print(f"✅ 合格且无'与步骤类型标签无关'样本数: {len(valid_samples_no_unrelated)}")
# print(f"✅ 合格且含有'与步骤类型标签无关'样本数: {len(valid_samples_with_unrelated)}")
# print(f"✅ 所有合格样本保存到: {valid_all_output_path}")
# print(f"❌ 不合法样本保存到: {invalid_output_path}")



import json
import random

# 输入路径
no_unrelated_path = "/data_train/code/mllm/zhangtao02/check/train_prm/sci50w_perfect_valid_no_unrelated.jsonl"
with_unrelated_path = "/data_train/code/mllm/zhangtao02/check/train_prm/sci50w_perfect_valid_with_unrelated.jsonl"

# 需要抽取的数量
sample_num = 30000

# no_unrelated_path = "/data_train/code/mllm/zhangtao02/check/train_prm/sci50w_error_valid_no_unrelated.jsonl"
# with_unrelated_path = "/data_train/code/mllm/zhangtao02/check/train_prm/sci50w_error_valid_with_unrelated.jsonl"
# sample_num = 45000

# 读取无unrelated的样本
no_unrelated_samples = []
with open(no_unrelated_path, "r", encoding="utf-8") as fin:
    for line in fin:
        try:
            sample = json.loads(line.strip())
            no_unrelated_samples.append(sample)
        except Exception as e:
            print(f"⚠️ 跳过无效行，错误: {e}")

# 检查样本是否够
if len(no_unrelated_samples) < sample_num:
    raise ValueError(f"❌ 样本数量不足，只找到 {len(no_unrelated_samples)} 条，无法抽取 {sample_num} 条。")

# 随机抽样
sampled_samples = random.sample(no_unrelated_samples, sample_num)

# 生成剩余样本
sampled_set = set(json.dumps(s, ensure_ascii=False) for s in sampled_samples)
remaining_samples = [s for s in no_unrelated_samples if json.dumps(s, ensure_ascii=False) not in sampled_set]

# 读取已有的with_unrelated样本
with_unrelated_samples = []
with open(with_unrelated_path, "r", encoding="utf-8") as fin:
    for line in fin:
        try:
            sample = json.loads(line.strip())
            with_unrelated_samples.append(sample)
        except Exception as e:
            print(f"⚠️ 跳过无效行，错误: {e}")

# 合并新加进去
merged_samples = with_unrelated_samples + sampled_samples

# 保存更新的 with_unrelated 文件（覆盖）
with open(with_unrelated_path, "w", encoding="utf-8") as fout:
    for sample in merged_samples:
        fout.write(json.dumps(sample, ensure_ascii=False) + "\n")

# 保存更新后的 no_unrelated 文件（覆盖）
with open(no_unrelated_path, "w", encoding="utf-8") as fout:
    for sample in remaining_samples:
        fout.write(json.dumps(sample, ensure_ascii=False) + "\n")

# 打印总结
print(f"✅ 成功从 {no_unrelated_path} 抽取 {sample_num} 条并追加到 {with_unrelated_path}")
print(f"✅ {no_unrelated_path} 中剩余 {len(remaining_samples)} 条")
print(f"✅ {with_unrelated_path} 中总计 {len(merged_samples)} 条")
