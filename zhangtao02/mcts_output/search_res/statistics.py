import json
import re
from collections import Counter

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
        # 去掉 Markdown ``` 包裹
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

    # 剥一层 [[[...]]] → [[...]]
    while isinstance(lst, list) and len(lst) == 1 and isinstance(lst[0], list):
        lst = lst[0]
    return lst if isinstance(lst, list) else None

def extract_error_labels(parsed_steps):
    """
    从 parsed_steps 中抽出所有非“步骤正确”的标签，返回 frozenset。
    """
    errs = set()
    for step in parsed_steps:
        # 只取前两个元素均为字符串的条目
        if (isinstance(step, list) 
                and len(step) >= 2 
                and isinstance(step[0], str) 
                and isinstance(step[1], str)
                and step[1] in valid_labels):
            if step[1] != "步骤正确":
                errs.add(step[1])
    return frozenset(errs)

输入文件路径（可修改为其他 5 个文件合并后的路径）
input_paths = [
    "/data_train/code/mllm/zhangtao02/check/sci_false_final.jsonl",
    "/data_train/code/mllm/zhangtao02/check/sci_true_final.jsonl"]


counter = Counter()
total = 0
valid_count = 0

for path in input_paths:
    with open(path, "r", encoding="utf-8") as fin:
        for line in fin:
            total += 1
            try:
                rec = json.loads(line)
            except:
                continue

            raw = rec.get("gpt2res")
            parsed = parse_str_to_list(raw)
            if not parsed:
                continue


# 打印结果
print(f"总行数: {total}")
print(f"有效解析条数: {valid_count}")
print("\n各标签组合出现次数（空集合表示“全对”）：")
for errs, cnt in counter.most_common():
    name = "全对" if not errs else "&".join(sorted(errs))
    print(f"{name}: {cnt}")
# import json
# from collections import Counter
# import re

# # 所有包含错误标签的文件列表
# file_paths = [
#     "/data_train/code/mllm/zhangtao02/mcts_output/search_res/mcts_sci_nonterminal_final.jsonl",
# ]

# # 合法标签列表
# valid_labels = [
#     "步骤正确", "图像认知错误", "题意理解错误", "缺乏相关知识",
#     "知识应用错误", "逻辑过程错误", "幻觉错误", "运算处理错误", "与步骤类型标签无关"
# ]

# def parse_gpt2res(raw):
#     # 如果已经解析过，可以直接取 gpt2res_parsed
#     if isinstance(raw, list):
#         return raw
#     # 否则尝试 eval/JSON 解析
#     txt = re.sub(r"^```(?:json|python)?|```$", "", raw or "", flags=re.IGNORECASE).strip()
#     try:
#         parsed = json.loads(txt)
#     except:
#         try:
#             parsed = eval(txt)
#         except:
#             return None
#     # 剥一层嵌套 [[[...]]] → [[...]]
#     while isinstance(parsed, list) and len(parsed) == 1 and isinstance(parsed[0], list):
#         parsed = parsed[0]
#     return parsed

# counter = Counter()

# for path in file_paths:
#     with open(path, encoding="utf-8") as f:
#         for line in f:
#             obj = json.loads(line)
#             raw = obj.get("gpt2res_parsed") or obj.get("gpt2res")
#             steps = parse_gpt2res(raw)
#             if not isinstance(steps, list):
#                 continue
#             for step in steps:
#                 if isinstance(step, list) and len(step) >= 2:
#                     tag = step[1]
#                     if tag in valid_labels:
#                         counter[tag] += 1

# # 打印每个标签的出现次数
# for label in valid_labels:
#     print(f"{label}: {counter[label]}")
# import json, re, random
# from collections import defaultdict, Counter

# random.seed(42)

# # 合法标签和步骤类型
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
#     把 gpt2res 字段（可能是 str 也可能是 list）解析成标准的 list[list[str,...]]。
#     自动剥除多余一层 [[[...]]] → [[...]]。
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

#     # 剥一层 [[[...]]] → [[...]]
#     while isinstance(lst, list) and len(lst) == 1 and isinstance(lst[0], list):
#         lst = lst[0]
#     return lst if isinstance(lst, list) else None

# def extract_error_labels(parsed_steps):
#     """
#     从 parsed_steps 中抽出所有非“步骤正确”的标签，返回 frozenset 作为组合 key。
#     """
#     errs = set()
#     for step in parsed_steps:
#         if (isinstance(step, list) and len(step) >= 2
#                 and isinstance(step[0], str) and isinstance(step[1], str)
#                 and step[1] in valid_labels):
#             if step[1] != "步骤正确":
#                 errs.add(step[1])
#     return frozenset(errs)

# # 1) 先把所有记录分桶
# input_paths = [
#     "/data_train/code/mllm/zhangtao02/mcts_output/search_res/72b_search_res_1_post0.jsonl",
#     "/data_train/code/mllm/zhangtao02/mcts_output/search_res/72b_search_res_2_post0.jsonl",
#     "/data_train/code/mllm/zhangtao02/mcts_output/search_res/72b_search_res_3_post0.jsonl",
#     "/data_train/code/mllm/zhangtao02/mcts_output/search_res/72b_search_res_4_post0.jsonl",
#     "/data_train/code/mllm/zhangtao02/mcts_output/search_res/72b_search_res_5_post0.jsonl",
# ]

# buckets = defaultdict(list)
# total = 0
# valid_parsed = 0

# for path in input_paths:
#     with open(path, "r", encoding="utf-8") as fin:
#         for line in fin:
#             total += 1
#             try:
#                 rec = json.loads(line)
#             except:
#                 continue

#             raw = rec.get("gpt2res")
#             parsed = parse_str_to_list(raw)
#             if not parsed:
#                 continue

#             # 验证步骤类型和标签合法性
#             ok = True
#             for step in parsed:
#                 if not (
#                     isinstance(step, list) and len(step) >= 2
#                     and isinstance(step[0], str) and isinstance(step[1], str)
#                     and step[0] in valid_steps and step[1] in valid_labels
#                 ):
#                     ok = False
#                     break
#             if not ok:
#                 continue

#             valid_parsed += 1
#             errs = extract_error_labels(parsed)
#             buckets[errs].append((rec, parsed))

# print(f"总行数: {total}")
# print(f"成功解析并合法条数: {valid_parsed}")
# print(f"出现的标签组合数: {len(buckets)}")

# # 2) 定义下采样方案
# sampling_plan = {
#     frozenset():                     100_000,  # 全对
#     frozenset({"知识应用错误","逻辑过程错误"}): 20_000,
#     frozenset({"知识应用错误"}):        10_000,
#     frozenset({"逻辑过程错误"}):        30_000,
#     frozenset({"与步骤类型标签无关"}):     48_923,
#     frozenset({"幻觉错误","知识应用错误","逻辑过程错误"}): 20_000,
#     frozenset({"知识应用错误","逻辑过程错误","题意理解错误"}): 20_000,
#     frozenset({"幻觉错误","逻辑过程错误"}): 15_000,
#     frozenset({"题意理解错误"}):      32_135,
#     frozenset({"知识应用错误","运算处理错误","逻辑过程错误"}): 15_000,
#     frozenset({"逻辑过程错误","题意理解错误"}): 15_000,
#     frozenset({"运算处理错误","逻辑过程错误"}): 15_000,
#     frozenset({"知识应用错误","缺乏相关知识","逻辑过程错误"}): 10_000,
#     frozenset({"幻觉错误","知识应用错误","逻辑过程错误","题意理解错误"}): 10_000,
#     # 其它组合不在这里列，就全部保留
# }

# # 3) 按计划抽样
# sampled = []
# for combo, recs in buckets.items():
#     if combo in sampling_plan:
#         k = sampling_plan[combo]
#         if len(recs) > k:
#             recs = random.sample(recs, k)
#     # 不在计划里的，直接全部加入
#     sampled.extend(recs)

# print(f"抽样后总条数: {len(sampled)}")

# # 4) 把处理后的 gpt2res（parsed list） 写回新文件
# out_path = "/data_train/code/mllm/zhangtao02/mcts_output/search_res/sample_processed.jsonl"
# with open(out_path, "w", encoding="utf-8") as fout:
#     for rec, parsed in sampled:
#         # 用解析好的 parsed 覆盖原字段
#         rec["gpt2res"] = parsed
#         fout.write(json.dumps(rec, ensure_ascii=False) + "\n")

# print(f"✅ 抽样并写入到：{out_path}")
# import json
# import random
# import re

# # 固定随机种子以保证可复现
# random.seed(42)

# # 输入输出路径
# INPUT = "/data_train/code/mllm/zhangtao02/mcts_output/search_res/sample_processed.jsonl"
# OUT1  = "/data_train/code/mllm/zhangtao02/mcts_output/search_res/sample_part1.jsonl"
# OUT2  = "/data_train/code/mllm/zhangtao02/mcts_output/search_res/sample_part2.jsonl"

# # 要保证全部出现在第一份的特殊标签
# VALID_LABEL = "与步骤类型标签无关"

# def parse_str_to_list(s):
#     """
#     将 gpt2res 字段（可能是 str 也可能是 list）解析成标准的 list[list[...]]，
#     并自动剥离多余的三层嵌套 [[[...]]] → [[...]]。
#     """
#     if isinstance(s, list):
#         lst = s
#     elif isinstance(s, str):
#         # 去掉 Markdown ``` 包裹
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

#     # 剥一层 [[[...]]] → [[...]]
#     while isinstance(lst, list) and len(lst) == 1 and isinstance(lst[0], list):
#         lst = lst[0]
#     return lst if isinstance(lst, list) else None

# def has_special(parsed):
#     """
#     检查 parsed（list of steps）中是否含有“与步骤类型标签无关”这个标签
#     """
#     for step in parsed:
#         if isinstance(step, list) and len(step) >= 2 and step[1] == VALID_LABEL:
#             return True
#     return False

# # 1) 读入所有记录
# records = []
# with open(INPUT, "r", encoding="utf-8") as fin:
#     for line in fin:
#         rec = json.loads(line)
#         parsed = parse_str_to_list(rec.get("gpt2res"))
#         if isinstance(parsed, list):
#             records.append((rec, parsed))

# total = len(records)
# half  = total // 2

# # 2) 分 special / others
# special = []
# others  = []
# for rec, parsed in records:
#     if has_special(parsed):
#         special.append((rec, parsed))
#     else:
#         others.append((rec, parsed))

# # 3) 随机打散 others
# random.shuffle(others)

# # 4) 组装两份，保证 special 全在第一份
# need = max(0, half - len(special))
# file1 = special + others[:need]
# file2 = others[need:]

# print(f"总记录数: {total}")
# print(f"包含“{VALID_LABEL}”的 special: {len(special)}")
# print(f"others: {len(others)}")
# print(f"第一份目标≈{half}，实际: {len(file1)}")
# print(f"第二份 实际: {len(file2)}")

# # 5) 写出两份文件
# with open(OUT1, "w", encoding="utf-8") as f1, \
#      open(OUT2, "w", encoding="utf-8") as f2:
#     for rec, _ in file1:
#         f1.write(json.dumps(rec, ensure_ascii=False) + "\n")
#     for rec, _ in file2:
#         f2.write(json.dumps(rec, ensure_ascii=False) + "\n")

# print(f"已写入两份文件：\n  {OUT1}\n  {OUT2}")
# import json
# import re
# from collections import Counter

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
#         # 去掉 Markdown ``` 包裹
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

#     # 剥一层 [[[...]]] → [[...]]
#     while isinstance(lst, list) and len(lst) == 1 and isinstance(lst[0], list):
#         lst = lst[0]
#     return lst if isinstance(lst, list) else None

# def extract_error_labels(parsed_steps):
#     """
#     从 parsed_steps 中抽出所有非“步骤正确”的标签，返回 frozenset。
#     """
#     errs = set()
#     for step in parsed_steps:
#         # 只取前两个元素均为字符串的条目
#         if (isinstance(step, list) 
#                 and len(step) >= 2 
#                 and isinstance(step[0], str) 
#                 and isinstance(step[1], str)
#                 and step[1] in valid_labels):
#             if step[1] != "步骤正确":
#                 errs.add(step[1])
#     return frozenset(errs)

# # 输入文件路径（可修改为其他 5 个文件合并后的路径）
# input_paths = [
#     "/data_train/code/mllm/zhangtao02/mcts_output/search_res/mcts_math_nonterminal.jsonl"]

# # 输出文件路径
# output_path = "/data_train/code/mllm/zhangtao02/check/train_prm/math_false2.jsonl"

# counter = Counter()
# total = 0
# error_count = 0

# # 保存包含错误的解析记录
# invalid_records = []

# for path in input_paths:
#     with open(path, "r", encoding="utf-8") as fin:
#         for line in fin:
#             total += 1
#             try:
#                 rec = json.loads(line)
#             except:
#                 continue

#             raw = rec.get("gpt2res")
#             parsed = parse_str_to_list(raw)
#             if not parsed:
#                 continue

#             # 验证每一步前两个元素均为合法字符串及标签/步骤
#             ok = True
#             for step in parsed:
#                 if not (isinstance(step, list) and len(step) >= 2
#                         and isinstance(step[0], str) and isinstance(step[1], str)
#                         and step[0] in valid_steps and step[1] in valid_labels):
#                     ok = False
#                     break
#             if not ok:
#                 continue

#             # 只保留含有错误标签的记录
#             errs = extract_error_labels(parsed)
#             if errs:  # 如果有错误标签（即 errs 非空）
#                 error_count += 1
#                 invalid_records.append(rec)
#                 counter[errs] += 1

# # 打印结果
# print(f"总行数: {total}")
# print(f"存在错误标签的解析条数: {error_count}")
# print("\n各标签组合出现次数：")
# for errs, cnt in counter.most_common():
#     name = "全对" if not errs else "&".join(sorted(errs))
#     print(f"{name}: {cnt}")

# # 保存含错误的记录到文件
# with open(output_path, "w", encoding="utf-8") as fout:
#     for record in invalid_records:
#         fout.write(json.dumps(record, ensure_ascii=False) + "\n")

# print(f"✅ 完成：已保存含错误标签的记录至 {output_path}")

import json
import re
from collections import Counter

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
        # 去掉 Markdown ``` 包裹
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

    # 剥一层 [[[...]]] → [[...]]
    while isinstance(lst, list) and len(lst) == 1 and isinstance(lst[0], list):
        lst = lst[0]
    return lst if isinstance(lst, list) else None

def extract_error_labels(parsed_steps):
    """
    从 parsed_steps 中抽出所有非“步骤正确”的标签（现在是第3个元素），返回 frozenset。
    """
    errs = set()
    for step in parsed_steps:
        # 每一项应该是四元组，并且第1列是valid_steps，第3列是valid_labels
        if (isinstance(step, list) 
                and len(step) >= 4 
                and isinstance(step[0], str) 
                and isinstance(step[2], str)
                and step[0] in valid_steps
                and step[2] in valid_labels):
            if step[2] != "步骤正确":
                errs.add(step[2])
    return frozenset(errs)

# 输入文件路径
input_paths = [
    "/data_train/code/mllm/zhangtao02/check/sci_50wllavacot0_final.jsonl",
    "/data_train/code/mllm/zhangtao02/check/sci_50wllavacot1_final.jsonl"
]

counter = Counter()
total = 0
valid_count = 0

for path in input_paths:
    with open(path, "r", encoding="utf-8") as fin:
        for line in fin:
            total += 1
            try:
                rec = json.loads(line)
            except:
                continue

            raw = rec.get("gpt2res")
            parsed = parse_str_to_list(raw)
            if not parsed:
                continue

            errs = extract_error_labels(parsed)
            counter[errs] += 1
            valid_count += 1

# 打印结果
print(f"总行数: {total}")
print(f"有效解析条数: {valid_count}")
print("\n各标签组合出现次数（空集合表示“全对”）：")
for errs, cnt in counter.most_common():
    name = "全对" if not errs else "&".join(sorted(errs))
    print(f"{name}: {cnt}")
