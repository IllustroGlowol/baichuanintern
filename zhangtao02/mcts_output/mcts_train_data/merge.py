import os
import json
from glob import glob

# 设置目标文件夹路径
folder_path = "/data_train/code/mllm/zhangtao02/mcts_output/mcts_train_data/"
# 匹配所有以 best_terminal_paths_ 开头的 .jsonl 文件
file_pattern = os.path.join(folder_path, "best_terminal_paths_*.jsonl")
file_list = sorted(glob(file_pattern))

# 输出合并文件路径
output_file = os.path.join(folder_path, "mcts_0414.jsonl")

# 合并文件
with open(output_file, "w", encoding="utf-8") as fout:
    for file_path in file_list:
        with open(file_path, "r", encoding="utf-8") as fin:
            for line in fin:
                fout.write(line)

print(f"✅ 成功合并 {len(file_list)} 个文件，保存为 {output_file}")
