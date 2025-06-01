import json
from tqdm import tqdm

# 读取输入文件
# input_path = "/data_train/code/mllm/zhangtao02/check/train_prm/sci50w_llavacot_error_valid_with_unrelated.jsonl"
# output_path = "/data_train/code/mllm/zhangtao02/check/sci/sci50w_llavacot_error_valid_with_unrelated_converted.jsonl"
# input_path = "/data_train/code/mllm/zhangtao02/check/train_prm/sci50w_llavacot_error_valid_no_unrelated.jsonl"
# output_path = "/data_train/code/mllm/zhangtao02/check/sci/sci50w_llavacot_error_valid_no_unrelated_converted.jsonl"
# input_path = "/data_train/code/mllm/zhangtao02/check/train_prm/sci50w_error_valid_no_unrelated.jsonl"
# output_path = "/data_train/code/mllm/zhangtao02/check/sci/sci50w_error_valid_no_unrelated_converted.jsonl"

# input_path = "/data_train/code/mllm/zhangtao02/check/train_prm/sci50w_perfect_valid_no_unrelated.jsonl"
# output_path = "/data_train/code/mllm/zhangtao02/check/sci/sci50w_perfect_valid_no_unrelated_converted.jsonl"
# input_path = "/data_train/code/mllm/zhangtao02/check/train_prm/sci50w_error_valid_with_unrelated.jsonl"
# output_path = "/data_train/code/mllm/zhangtao02/check/sci/sci50w_error_valid_with_unrelated_converted.jsonl"


input_path = "/data_train/code/mllm/zhangtao02/check/train_prm/sci50w_perfect_valid_with_unrelated.jsonl"
output_path = "/data_train/code/mllm/zhangtao02/check/sci/sci50w_perfect_valid_with_unrelated_converted.jsonl"

# 固定的角色定义头
# prefix_prompt = """
# #一、角色定义\n你是一个擅长评估学生试卷的专业阅卷老师。我会提供一个题目(问题+图片),一个学生的解题过程。题目中可能包含多个需要回答的子问题。你的任务是对"学生的解题过程"进行【步骤拆分】和【步骤评估】。\n\n

# #二、工作步骤:\n
# ## step1:阅读这道题目, 理解题目，思考如何推导出正确步骤和结果。\n
# ## step2:进行“【步骤拆分】”:对"学生的解题过程"进行“步骤拆分”,步骤拆分要按照原文。\n 
# ## step3:进行“步骤标记”:对\"拆分后的步骤\"进行“步骤标记”。\n“步骤标记”说明：步骤标记必须从["步骤正确", "图像认知错误", "题意理解错误", "缺乏相关知识", "知识应用错误", "逻辑过程错误", "幻觉错误", "运算处理错误"]list中的8个元素中选择其中一个作为标签，不要生成 “图像认知正确”、“分析合理”、“正确”等非标准标记。\n
# ###“步骤标记”标签分类和含义：\n
# 1）步骤正确：如果未出现以下7类任何错误类型，则标记为"步骤正确"。\n
# 2）图像认知错误:学生在理解图表、图形,物体或空间关系时出现的识别错误,常见如:坐标轴理解错误、几何形状误判、空间关系混淆或数值读取不准确等问题\n
# 3）题意理解错误:由于对题目要求、条件或关键信息的理解偏差导致的解题错误,常见如:对问题表述的误读、限制条件的忽视或题目要求的错误解读等。\n
# 4）缺乏相关知识:对题目所涉及的学科知识不了解或者未能有效整合领域知识,常见如:对知识的解读错误,或者用了错误的解题方法。\n
# 5）知识应用错误:因对相关学科概念、原理、公式或方法的掌握不足或理解偏差而导致的解题错误,常见如:错误使用概念、误用公式定理等。\n
# 6）逻辑过程错误:在推理论证过程中出现的系统性错误,常见如:前提条件使用不当、推理链条断裂、论据不足或论证方法错误等导致结论错误的情况。\n
# 7）幻觉错误:学生的步骤存在事实性错误,逻辑不一致或无根据的推断等情况。常见如:学生的回答与已知的客观事实相违背或者在逻辑上存在矛盾或不合理之处以及学生在没有足够依据的情况下做出不合理的推断。\n
# 8）运算处理错误:在数学运算或代数处理过程中出现的具体计算错误,常见如:基本四则运算错误、代数式变形错误、方程求解错误或因式分解不当等问题。\n
# ## step4:进行“步骤标记解释”:对“步骤标记“中你做出的分类结果进行简短解释。\n\n

# # 三、输入部分:\n
# * 输入的问题:{question_text}
# * 输入的学生解题过程: {student_steps}

# # 四、输出格式限制:\n
# ## 1.输出整体格式: [[步骤1内容,步骤1的步骤标记结果,步骤1的步骤标记解释结果],,,[步骤n的步骤标记结果,步骤n的步骤标记解释结果]]，说明: 为一个两层列表list。注意: 第一层列表数量为"步骤列表"的步骤数量，第二层是长度为3的列表。\n
# ## 2.输出第一层列表格式说明: 长度为输入“步骤列表”的step数量。\n
# ## 3.输出第二层列表格式说明: 元素数量长度为3的列表，每个元素务必为合法字符串。其中元素0内容为“步骤内容”，元素1内容为针对当前步骤的“步骤标记”类型结果，元素2内容为针对元素1“步骤标记”结果的简短解释。具体格式为:[步骤内容，“步骤标记”结果, “步骤标记解释”结果]。注意:仅仅指具体格式，禁止复制上面格式说明中的内容。\n
# ## 4.“步骤标记”结果务必从["步骤正确", "图像认知错误", "题意理解错误", "缺乏相关知识", "知识应用错误", "逻辑过程错误", "幻觉错误", "运算处理错误"]list中的8个元素选择其中一个，选择标准务必按照【“步骤标记”标签分类定义】,禁止“步骤标记”结果 出现类似:"步骤错误", "步骤标记错误"的模糊回答。务必从9元素列表里面选择答案。\n
# ## 5.务必确保输出结果是一个双层列表，且第二层列表元素数为3.\n
# ## 6.务必确保输出结果可用python的eval()函数解析。不要在指定的格式之外添加任何解释/内容。\n
# ## 7.请直接以 list 的形式返回，无需添加注释、markdown 包裹、说明文字。\n
# ## 8.必须返回一个 只有两层嵌套结构 的 list（不能多包一层），例如：[[...], [...], [...]]。禁止返回 [[[...], [...]]]\n", 
# """
prefix_prompt = """
#一、角色定义\n
你是一个擅长评估学生试卷的专业阅卷老师。我会提供一个题目(问题+图片),一个学生的解题过程步骤列表。题目中可能包含多个需要回答的子问题。你的任务是对\"学生的解题过程步骤列表\"进行评估打分。\n\n
#二、工作步骤:\n
## step1:阅读这道题目, 理解题目，思考如何推导出正确步骤和结果。\n
## step2:进行“步骤标记”:对"学生的解题过程步骤列表"中的每一步,认真进行“步骤标记”,进行分类。\n
“步骤标记”说明：步骤标记必须从["步骤正确", "图像认知错误", "题意理解错误", "缺乏相关知识", "知识应用错误", "逻辑过程错误", "幻觉错误", "运算处理错误","与步骤类型标签无关"]list中的9个元素中选择其中一个作为标签，不要生成 “图像认知正确”、“分析合理”、“正确”等非标准标记。\n\n
###“步骤标记”标签分类和含义：\n1）步骤正确：如果未出现以下8任何错误类型，则标记为"步骤正确"。\n2）图像认知错误:学生在理解图表、图形,物体或空间关系时出现的识别错误,常见如:坐标轴理解错误、几何形状误判、空间关系混淆或数值读取不准确等问题\n3）题意理解错误:由于对题目要求、条件或关键信息的理解偏差导致的解题错误,常见如:对问题表述的误读、限制条件的忽视或题目要求的错误解读等。\n4）缺乏相关知识:对题目所涉及的学科知识不了解或者未能有效整合领域知识,常见如:对知识的解读错误,或者用了错误的解题方法。\n5）知识应用错误:因对相关学科概念、原理、公式或方法的掌握不足或理解偏差而导致的解题错误,常见如:错误使用概念、误用公式定理等。\n6）逻辑过程错误:在推理论证过程中出现的系统性错误,常见如:前提条件使用不当、推理链条断裂、论据不足或论证方法错误等导致结论错误的情况。\n7）幻觉错误:学生的步骤存在事实性错误,逻辑不一致或无根据的推断等情况。常见如:学生的回答与已知的客观事实相违背或者在逻辑上存在矛盾或不合理之处以及学生在没有足够依据的情况下做出不合理的推断。\n8）运算处理错误:在数学运算或代数处理过程中出现的具体计算错误,常见如:基本四则运算错误、代数式变形错误、方程求解错误或因式分解不当等问题。\n9）与步骤类型标签无关:学生的步骤回答内容与步骤类型标签含义无关，比如在caption阶段内并没有描述图像或者进行了反思或总结。\n\n
###其中步骤类型标签类型和不同类型的步骤代表的具体含义如下：\n- caption：描述图片中与问题相关的元素。\n### 具体动作:1)结合图片和问题思考解题需要用到哪些图像中的视觉元素。2)尽可能详细描述图片中可能对解决问题需要用到的视觉元素，务必描述清晰，详细。\n- summary：High-level summary of the question and its key points\n### 具体动作:依据caption, 结合图片+问题,直接分析解题涉及的所有可能的:'技巧'和'知识点'。\n- thinking：完成解题并生成最终答案的“具体推理步骤”\n### 具体动作:依据'历史action',结合图片+问题,继续执行'历史action'后下一步你需要执行的推理步骤。\n1.如果“历史action”的最后一步是sub_task，则根据subtask每个细分子任务进行详细思考，得出答案。注意:务必和sub_task action中拆解的解题步骤一致。\n   2.如果“历史action”的最后一步是double_check，则从'历史action'中的不同的思考角度进一步思考，得出答案。\n- double_check：重新验证'历史action'中的所有内容。\n### 具体动作:依据'历史action',结合图片+问题,对所有action进行仔细验证和检查。case1: 如果正确则直接说对应action正确。**禁止解释其他内容,禁止推理,禁止深度思考,禁止先分析再总结,禁止分析next step**。\ncase2:如果存在错误则需要详细指出错误的点和原因。\n- answer：Provide the final answer to the question\n### 具体动作:输出question对应的答案，需要按照其指定要求，比如格式，内容。（answer步只需要判断最终答案是否正确，不需要考虑是否包含解题步骤）\n\n
## step3:进行“步骤标记解释”:对“步骤标记“中你做出的分类结果进行简短解释。\n\n
# 三、输入部分:\n
  输入的问题:{question_text}
  输入的学生解题过程列表:{student_steps}
# 四、输出格式限制:\n## 1.输出整体格式: [[步骤类型标签1,步骤1的标记结果,步骤1的步骤标记解释结果],,,[步骤类型标签,步骤n的标记结果,步骤n的步骤标记解释结果]]，说明: 为一个两层列表list。注意: 第一层列表数量为\"步骤列表\"的步骤数量，第二层是长度为4的列表。\n
## 2.输出第一层列表格式说明: 长度为输入“步骤列表”的step数量。\n
## 3.输出第二层列表格式说明: 元素数量长度为3的列表，每个元素务必为合法字符串。其中元素0内容为“步骤类型标签”，元素0保持输入内容不变【直接复制】，元素1内容为针对当前步骤的“步骤标记”类型结果，元素2为针对元素1“步骤标记”结果的简短解释。具体格式为:[步骤类型标签，“步骤标记”结果, “步骤标记解释”结果]。注意:仅仅指具体格式，禁止复制上面格式说明中的内容。\n
## 4.“步骤标记”结果务必从["步骤正确", "图像认知错误", "题意理解错误", "缺乏相关知识", "知识应用错误", "逻辑过程错误", "幻觉错误", "运算处理错误","与步骤类型标签无关"]list中的9个元素选择其中一个，选择标准务必按照【“步骤标记”标签分类定义】,禁止“步骤标记”结果 出现类似:"步骤错误", "步骤标记错误"的模糊回答。务必从9元素列表里面选择答案。\n
## 5.“步骤标记”只需要考虑当前步骤标签正确与否，禁止考虑到其他标签，例如在answer时只需考虑输出答案正确与否，不需要考虑解题步骤是否详细、是否理解题意等\n
## 6.务必确保输出结果是一个双层列表，且第二层列表元素数为3.\n
## 7.务必确保输出结果可用python的eval()函数解析。不要在指定的格式之外添加任何解释/内容。\n
## 8.请直接以 list 的形式返回，无需添加注释、markdown 包裹、说明文字。\n
## 9.必须返回一个 只有两层嵌套结构 的 list（不能多包一层），例如：[[...], [...], [...]]。禁止返回 [[[...], [...]]]\n",
"""
def match_gpt2res(path_nodes, gpt2res):
    assistant_steps = []
    path_map = {p[0]: p[1] for p in path_nodes if len(p) >= 2}
    for res in gpt2res:
        if len(res) >= 3:
            step_type = res[0]
            if step_type in path_map:
                assistant_steps.append([path_map[step_type], res[1], res[2]])
    return assistant_steps
# # 开始处理
with open(input_path, "r", encoding="utf-8") as fin, \
     open(output_path, "w", encoding="utf-8") as fout:
    
#     for line in tqdm(fin, desc="转换中"):
#         data = json.loads(line.strip())
        
#         conversations = data.get("conversations", [])
#         gpt2res = data.get("gpt2res", [])
#         images = data.get("image", [])
        
        # # 提取human问题内容
        # question_text = ""
        # for conv in conversations:
        #     if conv.get("from") == "human":
        #         question_text = conv.get("value", "")
        #         break

#         # 🟡 拼接 gpt2res 每个子项的第2个字段，组成 student 步骤文本
#         student_steps = "\n".join(
#     item[1] if isinstance(item[1], str) else json.dumps(item[1], ensure_ascii=False)
#     for item in gpt2res if len(item) > 1
# )
#         # 🟢 构造 assistant 回复：去掉每个子项的第一个字段
#         assistant_steps = [item[1:] for item in gpt2res if len(item) >= 3]

        # # 生成输入的学生解题过程列表（取gpt2res每条前两个元素）
        # student_steps = []
        # for item in gpt2res:
        #     if len(item) >= 2:
        #         student_steps.append([item[0], item[1]])

        # # 生成assistant回答内容（去掉每个gpt2res条目的第2个元素）
        # assistant_steps = []
        # for item in gpt2res:
        #     if len(item) >= 3:
        #         assistant_steps.append([item[0], item[2], item[3]])
    for line in tqdm(fin, desc="转换中"):
        data = json.loads(line.strip())

        conversations = data.get("conversations", [])
        path_nodes = data.get("path_nodes", [])
        gpt2res = data.get("gpt2res", [])
        images = data.get("image", [])

    #     # 取 human 的问题描述
        question_text = path_nodes[0][1]
        # student_steps = "\n".join(p[1] for p in path_nodes[1:] if len(p) > 1)
        # assistant_steps = match_gpt2res(path_nodes, gpt2res)

        # 学生解题过程列表: 去掉path_nodes的第一个(base)，每步取(步骤标签, 步骤内容)
        student_steps = []
        for node in path_nodes[1:]:
            if isinstance(node, list) and len(node) == 2:
                student_steps.append([node[0], node[1]])

        # gpt2res: 不做处理，直接用
        assistant_steps = gpt2res
        # 构造最终结构
        new_data = {
            "messages": [
                {
                    "role": "user",
                    "content": prefix_prompt.format(question_text=question_text,student_steps=student_steps)
                },
                {
                    "role": "assistant",
                    "content": json.dumps(assistant_steps, ensure_ascii=False)
                }
            ],
            "images": images
        }
        
        fout.write(json.dumps(new_data, ensure_ascii=False) + "\n")

print(f"✅ 转换完成，保存到 {output_path}")