import json
import re
import random
from collections import defaultdict

# ---------- 可按需修改 ----------
input_paths = [
    
    "/data_train/code/mllm/zhangtao02/mcts_output/search_res/mcts_72b_32b_search_res_final.jsonl",
    "/data_train/code/mllm/zhangtao02/mcts_output/search_res/mcts_32b_32b_search_res_final.jsonl"
]
output_path = "/data_train/code/mllm/zhangtao02/mcts_output/search_res/math_all_correct_max2_test.jsonl"
# --------------------------------

valid_labels = {
    "步骤正确", "图像认知错误", "题意理解错误", "缺乏相关知识",
    "知识应用错误", "逻辑过程错误", "幻觉错误", "运算处理错误",
    "与步骤类型标签无关"
}
valid_steps = {
    "summary", "caption", "sub_task", "thinking",
    "double_check", "answer", "reflection", "evaluate"
}

def parse_str_to_list(s):
    """解析 gpt2res 为 list[list[...]] 并剥离多余嵌套"""
    if isinstance(s, list):
        lst = s
    elif isinstance(s, str):
        txt = re.sub(r"^```(?:json|python)?|```$", "", s,
                     flags=re.IGNORECASE).strip()
        try:
            lst = json.loads(txt)
        except Exception:
            try:
                lst = eval(txt)
            except Exception:
                return None
    else:
        return None
    while isinstance(lst, list) and len(lst) == 1 and isinstance(lst[0], list):
        lst = lst[0]
    return lst if isinstance(lst, list) else None

def all_steps_correct(parsed_steps):
    """是否所有步骤均为‘步骤正确’"""
    for step in parsed_steps:
        if not (isinstance(step, list) and len(step) >= 2
                and isinstance(step[0], str) and isinstance(step[1], str)
                and step[0] in valid_steps and step[1] in valid_labels):
            return False
        if step[1] != "步骤正确":
            return False
    return True

# 收集每个 question_id 下所有“全对”记录
candidate_records = defaultdict(list)

for path in input_paths:
    with open(path, "r", encoding="utf-8") as fin:
        for line in fin:
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue

            parsed = parse_str_to_list(rec.get("gpt2res"))
            if not parsed or not all_steps_correct(parsed):
                continue

            qid = rec.get("question_id")
            if qid is not None:
                candidate_records[qid].append(rec)

# 对每个 qid，最多随机选两条
with open(output_path, "w", encoding="utf-8") as fout:
    total_saved = 0
    for qid, recs in candidate_records.items():
        selected = random.sample(recs, min(1, len(recs)))
        for r in selected:
            fout.write(json.dumps(r, ensure_ascii=False) + "\n")
        total_saved += len(selected)

print(f"已保存 {total_saved} 条“全对记录”，每个 qid 随机最多两条 到 {output_path}")
