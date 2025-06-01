import json
import re
import random
import hashlib
from collections import defaultdict

# ======== 自定义参数 ========
input_paths = [
    "/data_train/code/mllm/zcl/scitest/tree_output/all_trees.jsonl"    # 可以继续添加更多文件路径
]

output_path = "/data_train/code/mllm/zcl/scitest/tree_output/all_non_terminal_sample3.jsonl"

SIGNATURE_LEN = None          # None→整条路径；如需固定前 n 步，设为 n（如 4）
MAX_DFS_ITER = 500_000        # 每棵树 DFS 上限

# ======== 工具函数 ========
def strip_tags(text: str) -> str:
    return re.sub(r"</?[^>]+>", "", text).strip()

def hash_path_nodes(path_nodes):
    return hashlib.md5(
        json.dumps(path_nodes, ensure_ascii=False).encode("utf-8")
    ).hexdigest()

def get_signature(path_nodes, max_len: int | None = SIGNATURE_LEN):
    steps = [step for step, _ in path_nodes]
    return tuple(steps if max_len is None else steps[:max_len])

def build_node_tree(node_list):
    node_map = {n["node_id"]: n for n in node_list}
    children_map = defaultdict(list)
    for n in node_list:
        for cid in n.get("children_ids", []):
            children_map[n["node_id"]].append(cid)
    return node_map, children_map

def has_error(path_nodes) -> bool:
    return any("[ERROR]" in str(n.get("node_value", "")) for n in path_nodes)

# ======== DFS 搜索中间路径（非终止） ========
def find_all_non_terminal_paths(tree_nodes):
    node_map, children_map = build_node_tree(tree_nodes)
    root_nodes = [n for n in tree_nodes if n.get("parent_id") is None]
    if not root_nodes:
        return []

    all_paths, iter_cnt = [], 0
    stack = [(root, [], set()) for root in root_nodes]  # (node, path, visited)

    while stack:
        iter_cnt += 1
        if iter_cnt > MAX_DFS_ITER:
            return None  # 超限视为异常

        node, path, visited = stack.pop()
        nid = node["node_id"]
        if nid in visited:
            continue  # 跳过环

        new_path = path + [node]
        new_visited = visited | {nid}

        if not node.get("is_terminal", False) and len(new_path) >= 2:  # 保证 path 长度 ≥ 2
            all_paths.append(new_path)

        for cid in children_map.get(nid, []):
            child = node_map.get(cid)
            if child is not None:
                stack.append((child, new_path, new_visited))

    return all_paths

def extract_path_info(path_nodes, meta_info):
    path = [
        [n["node_action_name"], strip_tags(n.get("node_value", ""))]
        for n in path_nodes
    ]
    return {
        "question_id": meta_info["question_id"],
        "path_nodes": path,
        "is_terminal": False,
        "question": meta_info["question"],
        "ground_truth": meta_info["ground_truth"],
        "image": meta_info["image"],
        "path_hash": hash_path_nodes(path),
        "signature": get_signature(path),
        "path_len": len(path),
        "node_path_ids": [n["node_id"] for n in path_nodes],
    }

# ======== 主程序入口 ========
def main():
    sampled_total, bad_case_cnt, skip_error_cnt = [], 0, 0

    for input_path in input_paths:
        with open(input_path, "r", encoding="utf-8") as fin:
            for line in fin:
                data = json.loads(line.strip())
                qid = data["question_id"]
                tree = data.get("tree", [])

                meta_info = {
                    "question_id": qid,
                    "question": data.get("question", ""),
                    "ground_truth": data.get("info", {}).get("ground_truth", ""),
                    "image": data.get("info", {}).get("image", []),
                }

                try:
                    non_terminal_paths = find_all_non_terminal_paths(tree)
                    if non_terminal_paths is None:
                        bad_case_cnt += 1
                        continue
                except Exception:
                    bad_case_cnt += 1
                    continue

                filtered_paths = [
                    p for p in non_terminal_paths if not has_error(p)
                ]
                if len(filtered_paths) == 0:
                    continue

                selected_paths = random.sample(
                    filtered_paths, min(3, len(filtered_paths))
                )
                for path_nodes in selected_paths:
                    sampled_total.append(extract_path_info(path_nodes, meta_info))

    # 将所有数据写入文件
    with open(output_path, "w", encoding="utf-8") as fout:
        for item in sampled_total:
            fout.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(
        f"✅ 完成：写入 {len(sampled_total)} 条非终止路径（≥2步）；"
        f"跳过异常树 {bad_case_cnt} 条；"
        f"跳过含 [ERROR] 路径 {skip_error_cnt} 条（已纳入过滤）；"
        f"签名长度 = {'全部' if SIGNATURE_LEN is None else SIGNATURE_LEN}；"
        f"已保存至 {output_path}"
    )

if __name__ == "__main__":
    main()
