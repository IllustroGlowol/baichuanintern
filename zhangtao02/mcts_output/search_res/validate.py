import json
import re

# 合法标签和步骤类型
valid_labels = [
    "步骤正确", "图像认知错误", "题意理解错误", "缺乏相关知识",
    "知识应用错误", "逻辑过程错误", "幻觉错误", "运算处理错误", "与步骤类型标签无关"
]
valid_steps = {
    "summary", "caption", "sub_task", "thinking",
    "double_check", "answer", "reflection", "evaluate"
}

def parse_str_to_obj(s):
    try:
        return json.loads(s)
    except:
        try:
            return eval(s)
        except:
            return None

def normalize(raw):
    if isinstance(raw, list):
        parsed = raw
    elif isinstance(raw, str):
        txt = re.sub(r"^```(?:json|python)?|```$", "", raw, flags=re.IGNORECASE).strip()
        parsed = parse_str_to_obj(txt)
    else:
        return None
    # 剥一层 [[[...]]] → [[...]]
    while isinstance(parsed, list) and len(parsed) == 1 and isinstance(parsed[0], list):
        parsed = parsed[0]
    return parsed

def check_gpt2res(res):
    if not isinstance(res, list):
        return False, "最外层不是 list", False
    all_correct = True
    for idx, item in enumerate(res):
        if not isinstance(item, list):
            return False, f"第 {idx+1} 步不是 list", False
        if len(item) != 3:
            return False, f"第 {idx+1} 步长度不是 3", False
        step_type, tag, explain = item
        if not all(isinstance(x, str) for x in item):
            return False, f"第 {idx+1} 步存在非字符串元素", False
        if step_type not in valid_steps:
            return False, f"第 {idx+1} 步非法步骤类型: {step_type}", False
        if tag not in valid_labels:
            return False, f"第 {idx+1} 步非法标签: {tag}", False
        if not explain.strip():
            return False, f"第 {idx+1} 步解释为空", False
        if tag != "步骤正确":
            all_correct = False
    return True, "合法", all_correct

# 输入/输出文件路径
input_path = "/data_train/code/mllm/zhangtao02/mcts_output/search_res/72b_search_res_5_post0.jsonl"
fully_correct_path = "/data_train/code/mllm/zhangtao02/mcts_output/search_res/72b_search_res_5_fully_correct.jsonl"
partly_error_path = "/data_train/code/mllm/zhangtao02/mcts_output/search_res/72b_search_res_5_partly_error.jsonl"

total = ok_count = 0
fully_correct_count = 0
error_tagged_count = 0

with open(input_path, encoding="utf-8") as fin, \
     open(fully_correct_path, "w", encoding="utf-8") as f_full, \
     open(partly_error_path, "w", encoding="utf-8") as f_part:

    for lineno, line in enumerate(fin, 1):
        total += 1
        try:
            obj = json.loads(line)
        except:
            continue

        raw = obj.get("gpt2res")
        parsed = normalize(raw)
        if parsed is None:
            continue

        ok, reason, all_correct = check_gpt2res(parsed)
        if not ok:
            continue

        ok_count += 1
        # 将 parsed 重新赋回字段，保持一致
        obj["gpt2res_parsed"] = parsed

        if all_correct:
            fully_correct_count += 1
            f_full.write(json.dumps(obj, ensure_ascii=False) + "\n")
        else:
            error_tagged_count += 1
            f_part.write(json.dumps(obj, ensure_ascii=False) + "\n")

# 打印统计
print(f"总条目: {total}")
print(f"合规条目: {ok_count}")
print(f"  ├ 全部步骤“步骤正确”: {fully_correct_count} （已写入 {fully_correct_path}）")
print(f"  └ 部分步骤含错误标签: {error_tagged_count} （已写入 {partly_error_path}）")
