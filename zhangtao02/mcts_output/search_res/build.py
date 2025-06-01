# import json
# import re

# INPUT_PATH  = "/data_train/code/mllm/zhangtao02/mcts_output/search_res/sample_part2.jsonl"
# OUTPUT_PATH = "/data_train/code/mllm/zhangtao02/mcts_output/search_res/sample_part2_with_qa.jsonl"

# # 你提供的“角色定义 + 步骤拆分 + … + 输出格式”模板
# TEMPLATE = r"""
# #一、角色定义
# 你是一个擅长评估学生试卷的专业阅卷老师。我会提供一个题目(问题+图片),一个学生的解题过程。题目中可能包含多个需要回答的子问题。你的任务是对"学生的解题过程"进行步骤拆分和步骤评估。

# #二、工作步骤:
# ## step1:阅读这道题目, 理解题目，思考如何推导出正确步骤和结果。
# ## step2:进行“步骤拆分”:对"学生的解题过程"进行“步骤拆分”。
# ## step3:进行“步骤标记”:对"拆分后的步骤"进行“步骤标记”。
# “步骤标记”说明：步骤标记必须从["步骤正确","图像认知错误","题意理解错误","缺乏相关知识","知识应用错误","逻辑过程错误","幻觉错误","运算处理错误"]list中的8个元素中选择其中一个作为标签，不要生成 “图像认知正确”、“分析合理”、“正确”等非标准标记。
# ###“步骤标记”标签分类和含义：
# 1）步骤正确：如果未出现以下7类任何错误类型，则标记为"步骤正确"。
# 2）图像认知错误:学生在理解图表、图形,物体或空间关系时出现的识别错误,常见如:坐标轴理解错误、几何形状误判、空间关系混淆或数值读取不准确等问题
# 3）题意理解错误:由于对题目要求、条件或关键信息的理解偏差导致的解题错误,常见如:对问题表述的误读、限制条件的忽视或题目要求的错误解读等。
# 4）缺乏相关知识:对题目所涉及的学科知识不了解或者未能有效整合领域知识,常见如:对知识的解读错误,或者用了错误的解题方法。
# 5）知识应用错误:因对相关学科概念、原理、公式或方法的掌握不足或理解偏差而导致的解题错误,常见如:错误使用概念、误用公式定理等。
# 6）逻辑过程错误:在推理论证过程中出现的系统性错误,常见如:前提条件使用不当、推理链条断裂、论据不足或论证方法错误等导致结论错误的情况。
# 7）幻觉错误:学生的步骤存在事实性错误,逻辑不一致或无根据的推断等情况。常见如:学生的回答与已知的客观事实相违背或者在逻辑上存在矛盾或不合理之处以及学生在没有足够依据的情况下做出不合理的推断。
# 8）运算处理错误:在数学运算或代数处理过程中出现的具体计算错误,常见如:基本四则运算错误、代数式变形错误、方程求解错误或因式分解不当等问题。
# ## step4:进行“步骤标记解释”:对“步骤标记“中你做出的分类结果进行简短解释。

# # 三、输入部分:
# ## 1. 输入整体格式: 
# 输入的问题：文本加图像
# 输入的学生解题过程：文本
# ### 输入格式参考example【严格参考格式，忽略具体内容】:
# 输入的问题：同一直角坐标系中，一次函数y$_{1}$=k$_{1}$x+b与正比例函数y$_{2}$=k$_{2}$x的图象如图所示，则当y$_{1}$大于y$_{2}$时，x取值范围是（  ）\n$\\begin{description}\n\\item A. x＞0\\item B. x＜0\\item C. x＜-2\\item D. x＞-2\n\\end{description}$
# 输入的学生解题过程：这道题的目标是通过观察图像，确定在给定的条件下，哪个函数的值大于另一个函数的值。具体来说，要求找出y$_{1}$（一次函数）大于y$_{2}$（正比例函数）的x值范围。\n\n解决方法：\n1. 从图像中可以看出，一次函数y$_{1}$和正比例函数y$_{2}$分别在x=0的左侧和右侧相交。\n2. 我们需要找到y$_{1}$在x轴上方、y$_{2}$在x轴下方的区域。\n3. 观察图像，发现当x＜-2时，y$_{1}$的图像在y$_{2}$的图像上方，即y$_{1}$大于y$_{2}$。\n\n所以，正确答案是C. x＜-2。在这幅图像中，关键的视觉点包括交点（x=-2）以及函数的斜率方向：\n\n1. **交点（x=-2）**：这个点是两个函数的交点，表示在x=-2时，两个函数的y值相同。\n2. **函数的斜率方向**：\n   - 一次函数y¡=k¡x+b的斜率为负，表示这条线随着x的增加而向下倾斜。\n   - 正比例函数y=ky的斜率为正，表示这条线随着x的增加而向上倾斜。\n   \n因为要求出y¡大于y的x值范围，我们需要观察当y¡在上半部分（即在y的上方）时对应的x值。从图像中可以看出，当x小于-2时，y¡在y上方（即y¡大于y）。因此，正确答案是C. x＜-2。
#  以下是实际输入：
# * 输入的问题:{question}
# * 输入的学生解题过程:{student_answer}
# * 你可以参考另一位高级老师的解题思路:{ground_truth}，但是还是需要你自己从头开始做并判断，你自己的判断说明中不要提到【参考老师相关的信息】。

# # 四、输出格式限制:
# ## 1.输出整体格式: [[步骤内容,步骤1的标记结果,步骤1的步骤标记解释结果],,,[步骤n的标记结果,步骤n的步骤标记解释结果]]，说明: 为一个两层列表list。注意: 第一层列表数量为"步骤列表"的步骤数量，第二层是长度为3的列表。
# ### 格式参考example【严格参考格式，忽略具体内容】:
# [["summary", "这道题的目标是通过观察图像，确定在给定的条件下，哪个函数的值大于另一个函数的值。具体来说，要求找出y$_{1}$（一次函数）大于y$_{2}$（正比例函数）的x值范围。", "步骤正确", "准确总结了问题目标"],["caption", "解决方法：\n1. 从图像中可以看出，一次函数y$_{1}$和正比例函数y$_{2}$分别在x=0的左侧和右侧相交。\n2. 我们需要找到y$_{1}$在x轴上方、y$_{2}$在x轴下方的区域。\n3. 观察图像，发现当x＜-2时，y$_{1}$的图像在y$_{2}$的图像上方，即y$_{1}$大于y$_{2}$。", "步骤正确", "符合图像信息"],["thinking", "所以，正确答案是C. x＜-2。在这幅图像中，关键的视觉点包括交点（x=-2）以及函数的斜率方向：\n\n1. **交点（x=-2）**：这个点是两个函数的交点，表示在x=-2时，两个函数的y值相同。\n2. **函数的斜率方向**：\n   - 一次函数y¡=k¡x+b的斜率为负，表示这条线随着x的增加而向下倾斜。\n   - 正比例函数y=ky的斜率为正，表示这条线随着x的增加而向上倾斜。\n   \n因为要求出y¡大于y的x值范围，我们需要观察当y¡在上半部分（即在y的上方）时对应的x值。从图像中可以看出，当x小于-2时，y¡在y上方（即y¡大于y）。因此，正确答案是C. x＜-2。", "逻辑过程错误", "计算错误"]]

# ## 2.输出第一层列表格式说明: 长度为输入“步骤列表”的step数量。
# ## 3.输出第二层列表格式说明: 元素数量长度为3的列表，每个元素务必为合法字符串。其中元素0内容为步骤内容，元素1内容为针对当前步骤的“步骤标记”类型结果，元素2内容为针对元素1“步骤标记”结果的简短解释。具体格式为:[步骤内容，“步骤标记”结果, “步骤标记解释”结果]。注意:仅仅指具体格式，禁止复制上面格式说明中的内容。
# ## 4.“步骤标记”结果务必从["步骤正确", "图像认知错误", "题意理解错误", "缺乏相关知识", "知识应用错误", "逻辑过程错误", "幻觉错误", "运算处理错误"]list中的8个元素选择其中一个，选择标准务必按照【“步骤标记”标签分类定义】,禁止“步骤标记”结果 出现类似:"步骤错误", "步骤标记错误"的模糊回答。务必从9元素列表里面选择答案。
# ## 5.务必确保输出结果是一个双层列表，且第二层列表元素数为3.
# ## 6.务必确保输出结果可用python的eval()函数解析。不要在指定的格式之外添加任何解释/内容。
# ## 7.请直接以 list 的形式返回，无需添加注释、markdown 包裹、说明文字。
# ## 8.必须返回一个 **只有两层嵌套结构** 的 list（不能多包一层），例如：[[...], [...], [...]]。禁止返回 [[[...], [...]]]
# """

# def parse_gpt2res(raw):
#     """将 gpt2res 字段（可能是 str 或 list）统一解析为 Python list."""
#     if isinstance(raw, list):
#         return raw
#     if isinstance(raw, str):
#         txt = re.sub(r"^```(?:json|python)?|```$", "", raw, flags=re.IGNORECASE).strip()
#         try:
#             return json.loads(txt)
#         except:
#             try:
#                 return eval(txt)
#             except:
#                 return []
#     return []

# def build_question_a(path_nodes, ground_truth):
#     # 从 path_nodes 取出 question、student_answer
#     question = path_nodes[0][1]
#     student_answer = "\n".join(node[1] for node in path_nodes[1:])
#     # 用 replace 而非 format，避免模板中其他 {} 被误解析
#     text = TEMPLATE
#     text = text.replace("{question}", question)
#     text = text.replace("{student_answer}", student_answer)
#     text = text.replace("{ground_truth}", ground_truth)
#     return text

# with open(INPUT_PATH, "r", encoding="utf-8") as fin, \
#      open(OUTPUT_PATH, "w", encoding="utf-8") as fout:

#     for idx, line in enumerate(fin):
#         if idx >= 10:  # 只处理前10条
#             break

#         rec = json.loads(line)
#         pn  = rec.get("path_nodes", [])
#         gt  = rec.get("ground_truth", "")

#         # 构造 question_a
#         if isinstance(pn, list) and pn:
#             rec["question_a"] = build_question_a(pn, gt)

#         # 构造 answer_a: 用 path_nodes 后续内容 替换 gpt2res 每项的第一列
#         raw_res = rec.get("gpt2res", [])
#         parsed_res = parse_gpt2res(raw_res)
#         student_steps = [node[1] for node in pn[1:]]  # 跳过第一个 base
#         answer_a = []
#         for i, step in enumerate(parsed_res):
#             # step = [step_type, tag, explain]
#             tag = step[1] if len(step) > 1 else ""
#             explain = step[2] if len(step) > 2 else ""
#             content = student_steps[i] if i < len(student_steps) else ""
#             # 结果格式：[“步骤内容”, “步骤标记”, “解释”]
#             answer_a.append([content, tag, explain])

#         rec["answer_a"] = answer_a

#         fout.write(json.dumps(rec, ensure_ascii=False) + "\n")

# print("已处理前10条，输出写入：", OUTPUT_PATH)







import json

# 输入输出路径
input_path = "/data_train/code/mllm/zhangtao02/mcts_output/search_res/math_all_correct_max2_random.jsonl"
output_path = "/data_train/code/mllm/zcl/llamafactory/data/math_mcts_0424.jsonl"

with open(input_path, "r", encoding="utf-8") as fin, open(output_path, "w", encoding="utf-8") as fout:
    for line in fin:
        try:
            data = json.loads(line.strip())
        except json.JSONDecodeError:
            continue

        path_nodes = data.get("path_nodes", [])
        if not path_nodes or not isinstance(path_nodes, list) or len(path_nodes) < 2:
            continue

        user_content = path_nodes[0][1]  # 题干
        assistant_content = "\n".join(node[1] for node in path_nodes[1:] if len(node) > 1)

        new_record = {
            "messages": [
                {"role": "user", "content": user_content},
                {"role": "assistant", "content": assistant_content}
            ],
            "images": data.get("image", [])
        }

        fout.write(json.dumps(new_record, ensure_ascii=False) + "\n")

print(f"转换完成，已保存至 {output_path}")
