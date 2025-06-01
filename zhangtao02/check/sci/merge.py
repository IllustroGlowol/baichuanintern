# import json
# from pathlib import Path

# # 要合并的文件路径列表
# input_paths = [
#     "/data_train/code/mllm/zhangtao02/check/sci/sci50w_error_valid_no_unrelated_converted.jsonl",
#     "/data_train/code/mllm/zhangtao02/check/sci/sci50w_error_valid_with_unrelated_converted.jsonl",
#     "/data_train/code/mllm/zhangtao02/check/sci/sci50w_llavacot_error_valid_no_unrelated_converted.jsonl",
#     "/data_train/code/mllm/zhangtao02/check/sci/sci50w_llavacot_error_valid_with_unrelated_converted.jsonl",
#     "/data_train/code/mllm/zhangtao02/check/sci/sci50w_perfect_valid_with_unrelated_converted.jsonl",
#     "/data_train/code/mllm/zhangtao02/check/sci/sci50w_perfect_valid_no_unrelated_converted.jsonl"
# ]

# # 输出路径
# output_path = "/data_train/code/mllm/zcl/llamafactory/data/sciprm0430.jsonl"

# # 合并过程
# with open(output_path, "w", encoding="utf-8") as fout:
#     for path in input_paths:
#         path_obj = Path(path)
#         if not path_obj.exists():
#             print(f"⚠️ 文件不存在: {path}")
#             continue
#         with open(path_obj, "r", encoding="utf-8") as fin:
#             for line in fin:
#                 line = line.strip()
#                 if line:
#                     fout.write(line + "\n")

# print(f"✅ 合并完成，共合并 {len(input_paths)} 个文件，输出至: {output_path}")
import json

input_path = "/data_train/code/mllm/zcl/llamafactory/data/sciprm0430.jsonl"
output_path = "/data_train/code/mllm/zcl/llamafactory/data/sciprm0430_fixed.jsonl"

def remove_existing_image_tokens(text):
    return text.replace("<image>", "").replace("<image/>", "").replace("< image >", "").strip()

def insert_image_tokens(message_text, num_images):
    return message_text + "\n" + "\n".join(["<image>"] * num_images)

with open(input_path, "r", encoding="utf-8") as f_in, open(output_path, "w", encoding="utf-8") as f_out:
    for line in f_in:
        data = json.loads(line)
        messages = data.get("messages", [])
        images = data.get("images", [])

        if messages and images:
            new_messages = []
            for m in messages:
                if m["role"] == "user":
                    # 清除原本的 <image> 标签
                    cleaned_text = remove_existing_image_tokens(m["content"])
                    # 重新添加正确数量的 <image>
                    updated_text = insert_image_tokens(cleaned_text, len(images))
                    m["content"] = updated_text
                new_messages.append(m)
            data["messages"] = new_messages

        f_out.write(json.dumps(data, ensure_ascii=False) + "\n")

print(f"✅ 修复完成，结果已保存至：{output_path}")
