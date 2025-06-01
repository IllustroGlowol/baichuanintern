import json
import re
from collections import Counter
from tqdm import tqdm

# 合法标签与步骤类型
valid_labels = {
    "步骤正确", "图像认知错误", "题意理解错误", "缺乏相关知识",
    "知识应用错误", "逻辑过程错误", "幻觉错误", "运算处理错误", "与步骤类型标签无关"
}
valid_steps = {
    "summary", "caption", "sub_task", "thinking",
    "double_check", "answer", "reflection", "evaluate"
}

def parse_str_to_list(s):
    """
    把 gpt2res 字段（可能是 str 也可能是 list）解析成标准的 list[list[...]]。
    自动剥离多余的三层嵌套。
    """
    if isinstance(s, list):
        lst = s
    elif isinstance(s, str):
        txt = re.sub(r"^```(?:json|python)?|```$", "", s, flags=re.IGNORECASE).strip()
        try:
            lst = json.loads(txt)
        except:
            try:
                lst = eval(txt)
            except:
                return None
    else:
        return None

    while isinstance(lst, list) and len(lst) == 1 and isinstance(lst[0], list):
        lst = lst[0]
    return lst if isinstance(lst, list) else None

def extract_error_labels(parsed_steps):
    """
    从 parsed_steps 中抽出所有非“步骤正确”的标签，返回 frozenset。
    """
    errs = set()
    for step in parsed_steps:
        if (isinstance(step, list) 
                and len(step) >= 2 
                and isinstance(step[0], str) 
                and isinstance(step[1], str)
                and step[1] in valid_labels):
            if step[1] != "步骤正确":
                errs.add(step[1])
    return frozenset(errs)

def convert_sets_to_lists(obj):
    """
    把对象中的 set / frozenset 全部转成 list，避免 JSON 序列化报错。
    """
    if isinstance(obj, dict):
        return {k: convert_sets_to_lists(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_sets_to_lists(v) for v in obj]
    elif isinstance(obj, (set, frozenset)):
        return list(obj)
    elif obj is Ellipsis:  # Handle ellipsis
        return None  # You can replace it with None or an empty list if needed
    else:
        return obj

# 输入文件路径（可以改）
input_paths = [
    "/data_train/code/mllm/zhangtao02/check/math_false_final.jsonl",
    "/data_train/code/mllm/zhangtao02/check/math_true_final.jsonl"
]

output_perfect = "/data_train/code/mllm/zhangtao02/check/train_prm/math13w_perfect.jsonl"
output_error = "/data_train/code/mllm/zhangtao02/check/train_prm/math13w_error.jsonl"

counter = Counter()
total = 0
valid_count = 0
perfect_count = 0
error_count = 0

# 计算总行数，方便 tqdm 显示
total_lines = 0
for path in input_paths:
    with open(path, "r", encoding="utf-8") as f:
        total_lines += sum(1 for _ in f)

# 打开输出文件
with open(output_perfect, "w", encoding="utf-8") as fout_perfect, \
     open(output_error, "w", encoding="utf-8") as fout_error:

    with tqdm(total=total_lines, desc="Processing") as pbar:
        for path in input_paths:
            with open(path, "r", encoding="utf-8") as fin:
                for line in fin:
                    total += 1
                    pbar.update(1)

                    try:
                        rec = json.loads(line)
                    except:
                        continue

                    raw = rec.get("gpt2res")
                    parsed = parse_str_to_list(raw)
                    if not parsed:
                        continue

                    valid_count += 1
                    errs = extract_error_labels(parsed)

                    # 更新 rec，把 gpt2res 字段替换成解析后的内容
                    rec["gpt2res"] = parsed

                    # sanitize or convert sets to lists
                    rec = convert_sets_to_lists(rec)

                    # Write to output files
                    try:
                        if not errs:
                            perfect_count += 1
                            json.dump(rec, fout_perfect, ensure_ascii=False)
                            fout_perfect.write("\n")
                        else:
                            error_count += 1
                            json.dump(rec, fout_error, ensure_ascii=False)
                            fout_error.write("\n")
                    except TypeError as e:
                        print(f"Error serializing record: {rec}")
                        print(f"Error: {e}")

                    # 更新计数器
                    counter[errs] += 1

# 打印统计结果
print("\n========== 总结 ==========")
print(f"总行数: {total}")
print(f"有效解析条数: {valid_count}")
print(f"全对样本数: {perfect_count}")
print(f"出错样本数: {error_count}")
print("\n各标签组合出现次数（空集合表示“全对”）：")
for errs, cnt in counter.most_common():
    name = "全对" if not errs else "&".join(sorted(errs))
    print(f"{name}: {cnt}")

# import json
# import re
# from collections import Counter
# from tqdm import tqdm

# # 合法标签与步骤类型
# valid_labels = {
#     "步骤正确", "图像认知错误", "题意理解错误", "缺乏相关知识",
#     "知识应用错误", "逻辑过程错误", "幻觉错误", "运算处理错误", "与步骤类型标签无关"
# }
# valid_steps = {
#     "summary", "caption", "sub_task", "thinking",
#     "double_check", "answer", "reflection", "evaluate"
# }

# def parse_str_to_list(s):
#     """
#     把 gpt2res 字段（可能是 str 也可能是 list）解析成标准的 list[list[...]]。
#     自动剥离多余的三层嵌套。
#     """
#     if isinstance(s, list):
#         lst = s
#     elif isinstance(s, str):
#         txt = re.sub(r"^```(?:json|python)?|```$", "", s, flags=re.IGNORECASE).strip()
#         try:
#             lst = json.loads(txt)
#         except:
#             try:
#                 lst = eval(txt)
#             except:
#                 return None
#     else:
#         return None

#     while isinstance(lst, list) and len(lst) == 1 and isinstance(lst[0], list):
#         lst = lst[0]
#     return lst if isinstance(lst, list) else None

# def extract_error_labels(parsed_steps):
#     """
#     从 parsed_steps 中抽出所有非“步骤正确”的标签（现在是第3个元素），返回 frozenset。
#     """
#     errs = set()
#     for step in parsed_steps:
#         if (isinstance(step, list) 
#                 and len(step) >= 4 
#                 and isinstance(step[0], str) 
#                 and isinstance(step[2], str)
#                 and step[0] in valid_steps
#                 and step[2] in valid_labels):
#             if step[2] != "步骤正确":
#                 errs.add(step[2])
#     return frozenset(errs)

# def convert_sets_to_lists(obj):
#     """
#     把对象中的 set / frozenset 全部转成 list，避免 JSON 序列化报错。
#     """
#     if isinstance(obj, dict):
#         return {k: convert_sets_to_lists(v) for k, v in obj.items()}
#     elif isinstance(obj, list):
#         return [convert_sets_to_lists(v) for v in obj]
#     elif isinstance(obj, (set, frozenset)):
#         return list(obj)
#     else:
#         return obj

# # 输入文件路径
# input_paths = [
#     "/data_train/code/mllm/zhangtao02/check/math_13wllavacot0_final.jsonl",
#     "/data_train/code/mllm/zhangtao02/check/math_13wllavacot1_final.jsonl"
# ]

# # 输出文件路径
# output_perfect = "/data_train/code/mllm/zhangtao02/check/train_prm/math13w_llavacot_perfect.jsonl"
# output_error = "/data_train/code/mllm/zhangtao02/check/train_prm/math13w_llavacot_error.jsonl"

# counter = Counter()
# total = 0
# valid_count = 0
# perfect_count = 0
# error_count = 0

# # 预计算总行数，用于tqdm显示进度
# total_lines = 0
# for path in input_paths:
#     with open(path, "r", encoding="utf-8") as f:
#         total_lines += sum(1 for _ in f)

# # 开始处理
# with open(output_perfect, "w", encoding="utf-8") as fout_perfect, \
#      open(output_error, "w", encoding="utf-8") as fout_error:

#     with tqdm(total=total_lines, desc="Processing") as pbar:
#         for path in input_paths:
#             with open(path, "r", encoding="utf-8") as fin:
#                 for line in fin:
#                     total += 1
#                     pbar.update(1)

#                     try:
#                         rec = json.loads(line)
#                     except:
#                         continue

#                     raw = rec.get("gpt2res")
#                     parsed = parse_str_to_list(raw)
#                     if not parsed:
#                         continue

#                     valid_count += 1
#                     errs = extract_error_labels(parsed)

#                     # 更新 gpt2res 字段为解析后的版本
#                     rec["gpt2res"] = parsed

#                     # 保存前防止 set 类型
#                     rec = convert_sets_to_lists(rec)

#                     if not errs:
#                         perfect_count += 1
#                         json.dump(rec, fout_perfect, ensure_ascii=False)
#                         fout_perfect.write("\n")
#                     else:
#                         error_count += 1
#                         json.dump(rec, fout_error, ensure_ascii=False)
#                         fout_error.write("\n")

#                     counter[errs] += 1

# # 打印统计信息
# print("\n========== 总结 ==========")
# print(f"总行数: {total}")
# print(f"有效解析条数: {valid_count}")
# print(f"全对样本数: {perfect_count}")
# print(f"出错样本数: {error_count}")
# print("\n各标签组合出现次数（空集合表示“全对”）：")
# for errs, cnt in counter.most_common():
#     name = "全对" if not errs else "&".join(sorted(errs))
#     print(f"{name}: {cnt}")
