from opencc import OpenCC  # 用于简繁转换
import re
import os

# 初始化OpenCC进行繁体到简体的转换
cc = OpenCC('t2s')  # 使用繁体到简体转换器

def compare_texts(recognized_text, target_text):
    """比较两个文本字符串，并返回差异信息"""
    if recognized_text == target_text:
        return "完全相同", None
    
    if len(recognized_text) == len(target_text):
        diff_info = []
        for i, (r_char, t_char) in enumerate(zip(recognized_text, target_text)):
            if r_char != t_char:
                diff_info.append(f"位置{i}：目标：{t_char}，识别：{r_char}")
        return "长度相同但有差异", "\n".join(diff_info)
    
    # 处理长度不一致的情况
    min_len = min(len(recognized_text), len(target_text))
    prefix_length = 0
    suffix_length = 0
    for i in range(min_len):
        if recognized_text[i] == target_text[i]:
            prefix_length += 1
        else:
            break
    for i in range(1, min_len + 1):
        if recognized_text[-i] == target_text[-i]:
            suffix_length += 1
        else:
            break
    
    middle_recognized = recognized_text[prefix_length:len(recognized_text)-suffix_length]
    middle_target = target_text[prefix_length:len(target_text)-suffix_length]
    
    middle_diff = []
    for i, (r_char, t_char) in enumerate(zip(middle_recognized, middle_target)):
        if r_char != t_char:
            middle_diff.append(f"中间部分位置{i}：目标：{t_char}，识别：{r_char}")
    
    diff_message = f"前缀匹配长度：{prefix_length}\n后缀匹配长度：{suffix_length}"
    if middle_diff:
        diff_message += "\n" + "\n".join(middle_diff)
    
    return "长度不一致", diff_message

# 结果保存文件
output_file = 'recognition_results.txt'
comparison_file = 'comparison_results.html'

# 读取文本文件内容
with open('../qldzj-ml/3.sutra-name-list.txt', 'r', encoding='utf-8') as file:
    target_lines = file.read().splitlines()

# 读取recognition_results.txt内容
with open(output_file, 'r', encoding='utf-8') as file:
    recognition_results = file.readlines()

# 生成新的比较结果HTML
html_table = "<table border='1'><tr><th>相对目录</th><th>目标文本</th><th>识别文本（简体）</th><th>差异</th></tr>"

# 假设recognition_results每一行格式为 "relative_path：recognized_text\n"
for result_line in recognition_results:
    parts = result_line.strip().split("：")
    relative_path = parts[0]
    recognized_text = parts[1] if len(parts) > 1 else ""
    simplified_text = cc.convert(recognized_text)  # 转换为简体字
    
    # 获取对应的目标文本
    image_name = os.path.basename(relative_path)
    image_dir = os.path.dirname(relative_path)
    processed_images_index = int(os.path.splitext(image_name)[0]) - 1  # 假设图片名是索引值
    target_text = target_lines[processed_images_index] if processed_images_index < len(target_lines) else ""

    comparison_result, diff_details = compare_texts(simplified_text, target_text)
    
    html_table += f"<tr><td>{relative_path}</td><td>{target_text}</td><td>{simplified_text}</td><td>{comparison_result}<br>{diff_details}</td></tr>"

html_table += "</table>"

with open(comparison_file, 'w', encoding='utf-8') as file:
    file.write(html_table)

print(f"详细的比较结果已保存到 {comparison_file}")
