# import json
# import os
# import shutil
# from tqdm import tqdm  # 引入 tqdm 库用于进度条
# from concurrent.futures import ThreadPoolExecutor  # 用于并行化操作

# # 原文件路径
# input_file_path = "/data_train/code/mllm/zcl/data_construct/100w_mcts_pre.jsonl"
# # 目标目录
# output_base_dir = "/global_data/mllm/zcl"
# # 跳过文件的日志路径
# skip_log_path = "/global_data/mllm/zcl/skipped_files.log"

# # 目标路径的文件夹创建
# def create_target_directory(file_path):
#     target_dir = os.path.dirname(file_path)
#     if not os.path.exists(target_dir):
#         os.makedirs(target_dir)

# # 复制图片
# def copy_image(src_path, dest_path, skip_log):
#     # 如果目标文件已存在，跳过复制
#     if os.path.exists(dest_path):
#         return f"目标文件 {dest_path} 已存在，跳过复制。"

#     # 如果源文件存在，进行复制
#     if os.path.exists(src_path):
#         create_target_directory(dest_path)  # 创建目标文件夹
#         shutil.copy(src_path, dest_path)  # 复制文件
#         return f"图片 {src_path} 已复制到 {dest_path}"
#     else:
#         # 如果文件不存在，记录到日志文件
#         with open(skip_log, 'a', encoding='utf-8') as log_file:
#             log_file.write(f"源文件 {src_path} 不存在，跳过复制。\n")
#         return f"源文件 {src_path} 不存在，跳过复制。"

# # 读取 JSONL 文件并处理每一条记录
# def process_file_line(line, skip_log_path, output_base_dir):
#     try:
#         record = json.loads(line)  # 解析 JSON 数据
#         image_paths = record.get("image", [])
        
#         results = []
#         for image_path in image_paths:
#             if image_path:
#                 # 保持路径结构不变，直接拼接到目标目录
#                 target_path = os.path.join(output_base_dir, image_path.lstrip('/data_train/mllm/lichong_02'))
                
#                 # 复制图片到目标路径
#                 result = copy_image(image_path, target_path, skip_log_path)
#                 results.append(result)
#         return results
#     except json.JSONDecodeError:
#         return [f"跳过解析错误的行: {line}"]

# # 读取 JSONL 文件并并行处理
# def process_all_files(input_file_path, skip_log_path, output_base_dir):
#     with open(input_file_path, 'r', encoding='utf-8') as f:
#         lines = f.readlines()  # 一次性读取所有行
#         total_lines = len(lines)  # 计算总行数

#         with tqdm(total=total_lines, desc="Processing images") as pbar:
#             with ThreadPoolExecutor() as executor:  # 使用线程池并行处理文件
#                 futures = []
#                 for line in lines:
#                     future = executor.submit(process_file_line, line, skip_log_path, output_base_dir)
#                     futures.append(future)

#                 # 获取线程执行的结果并更新进度条
#                 for future in futures:
#                     results = future.result()
#                     pbar.update(1)  # 更新进度条
#                     for result in results:
#                         print(result)

# # 执行文件处理
# process_all_files(input_file_path, skip_log_path, output_base_dir)
# import os
# import json

# # 输入和输出文件路径
# input_path = "/data_train/code/mllm/zhangtao02/EDUBench/data/3w.jsonl"
# output_path = "/data_train/code/mllm/zhangtao02/EDUBench/data/3w_modified.jsonl"

# old_prefix = "/data_train/mllm/lichong_02/afanti_all/qmat/chemistry-g12/pictures/"
# new_prefix = "/data_train/code/mllm/lichong/EDUBench/data/pictures/"

# with open(input_path, "r", encoding="utf-8") as fin, \
#      open(output_path, "w", encoding="utf-8") as fout:
#     for line in fin:
#         try:
#             sample = json.loads(line)
#             if "image" in sample and sample["image"].startswith(old_prefix):
#                 sample["image"] = sample["image"].replace(old_prefix, new_prefix, 1)
#             fout.write(json.dumps(sample, ensure_ascii=False) + "\n")
#         except Exception as e:
#             print(f"[解析失败] {e}")
# import json

# # 定义文件路径
# input_file_path = '/data_train/code/mllm/zcl/llamafactory/data/llavacot100w.jsonl'
# output_file_path = '/data_train/code/mllm/zcl/llamafactory/data/modified_raw100w.jsonl'

# # 读取文件并进行修改
# with open(input_file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8') as outfile:
#     for line in infile:
#         try:
#             # 加载当前行的 JSON 数据
#             data = json.loads(line)
            
#             # 修改 images 中的路径前缀
#             if 'images' in data:
#                 data['images'] = [img.replace('/data_train/mllm/lichong_02/afanti_all/', '/global_data/mllm/zcl/afanti_all/') for img in data['images']]
            
#             # 写入修改后的数据
#             outfile.write(json.dumps(data, ensure_ascii=False) + '\n')
#         except json.JSONDecodeError as e:
#             print(f"Error decoding JSON: {e}")
#         except Exception as e:
#             print(f"Error processing line: {e}")
import json
import os

# 配置
# input_path = "/data_train/code/mllm/zcl/llamafactory/data/llavacot100w.jsonl"
input_path = "/data_train/code/mllm/zcl/llamafactory/data/raw100w.jsonl"
temp_path = input_path + ".tmp"  # 临时文件路径
target_image = "/global_data/mllm/zcl/afanti_all/qmat/geography-g12/pictures/2023-10-31-geography-g12-00007_c17077e8b553970e02a85424fabfac86.png"

removed, kept = 0, 0

with open(input_path, "r", encoding="utf-8") as fin, \
     open(temp_path, "w", encoding="utf-8") as fout:
    for line in fin:
        try:
            sample = json.loads(line)
            if "images" in sample and target_image in sample["images"]:
                removed += 1
                continue
            fout.write(json.dumps(sample, ensure_ascii=False) + "\n")
            kept += 1
        except Exception:
            continue

# 替换原文件
os.replace(temp_path, input_path)

print(f"✅ 覆盖完成：已从原文件中移除 {removed} 条样本，保留 {kept} 条。")

# import os
# import json
# from tqdm import tqdm

# # === 配置路径 ===
# jsonl_path = "/data_train/code/mllm/zcl/llamafactory/data/raw100w.jsonl"
# root_image_dir = "/global_data/mllm/zcl/afanti_all/qmat"
# output_path = jsonl_path.replace(".jsonl", "_no_missing_image.jsonl")
# missing_path = jsonl_path.replace(".jsonl", "_missing_images.jsonl")

# # === 第一步：构建现有图片路径全集 ===
# print("📂 正在扫描实际存在的图片路径...")
# existing_images = set()
# for root, _, files in os.walk(root_image_dir):
#     for fname in files:
#         if fname.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
#             full_path = os.path.join(root, fname)
#             existing_images.add(full_path)

# print(f"✅ 图片扫描完成，共 {len(existing_images)} 张图片存在。")

# # === 第二步：清洗 JSONL 样本 ===
# kept, removed = 0, 0

# with open(jsonl_path, "r", encoding="utf-8") as fin, \
#      open(output_path, "w", encoding="utf-8") as fout_ok, \
#      open(missing_path, "w", encoding="utf-8") as fout_bad:

#     for line in tqdm(fin, desc="过滤含缺失图片的样本"):
#         try:
#             sample = json.loads(line)
#             imgs = sample.get("images", [])
#             if not isinstance(imgs, list):
#                 imgs = []

#             if any(img_path not in existing_images for img_path in imgs):
#                 fout_bad.write(json.dumps(sample, ensure_ascii=False) + "\n")
#                 removed += 1
#             else:
#                 fout_ok.write(json.dumps(sample, ensure_ascii=False) + "\n")
#                 kept += 1
#         except Exception:
#             removed += 1

# print(f"\n🎉 清洗完成：保留 {kept} 条，移除 {removed} 条。")
# print(f"✔ 合法样本保存到：{output_path}")
# print(f"⚠ 缺失图片样本保存到：{missing_path}")

# import os
# import json
# from tqdm import tqdm

# # 路径配置
# cleaned_jsonl = "/data_train/code/mllm/zcl/llamafactory/data/llavacot100w.jsonl"
# root_image_dir = "/global_data/mllm/zcl/afanti_all/qmat"

# # 加载现有图片路径
# print("重新加载所有存在图片路径进行验证...")
# existing_images = set()
# for root, _, files in os.walk(root_image_dir):
#     for fname in files:
#         if fname.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif','.bmp')):
#             existing_images.add(os.path.join(root, fname))

# print(f"图片加载完成，共 {len(existing_images)} 张。")

# # 验证 JSONL 是否还有未被清理干净的
# residual_bad = []
# with open(cleaned_jsonl, "r", encoding="utf-8") as f:
#     for idx, line in enumerate(tqdm(f, desc="二次验证样本中图片是否都存在")):
#         try:
#             data = json.loads(line)
#             imgs = data.get("images", [])
#             if any(p not in existing_images for p in imgs):
#                 residual_bad.append((idx, imgs))
#         except Exception:
#             continue

# if residual_bad:
#     print(f"\n警告：发现 {len(residual_bad)} 条样本中仍含不存在的图片路径，例如：")
#     for i, paths in residual_bad[:5]:
#         print(f"  - 行 {i}: 缺失路径示例 {paths}")
# else:
#     print("\n验证通过：所有样本引用的图片路径都存在，检查彻底完成！")

