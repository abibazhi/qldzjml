from opencc import OpenCC  # 用于简繁转换

# 初始化OpenCC进行繁体到简体的转换
cc = OpenCC('t2s')  # 使用繁体到简体转换器

# 结果保存文件
output_file = 'recognition_results.txt'
comparison_file = 'comparison_results.html'
standard_text_file = '../qldzj-ml/3.sutra-name-list.txt'

# 读取标准文本内容
with open(standard_text_file, 'r', encoding='utf-8') as file:
    target_lines = file.read().splitlines()

# 读取recognition_results.txt内容
with open(output_file, 'r', encoding='utf-8') as file:
    recognition_results = file.readlines()

# 创建HTML表格
html_table = "<table border='1'><tr><th>相对目录</th><th>目标文本</th><th>识别文本（简体）</th><th>比较结果</th></tr>"

# 遍历每一行识别结果
for index, result_line in enumerate(recognition_results):
    parts = result_line.strip().split("：")
    relative_path = parts[0]
    recognized_text = parts[1] if len(parts) > 1 else ""
    
    # 将识别结果转换为简体字
    simplified_recognized_text = cc.convert(recognized_text)
    
    # 获取对应的目标文本
    if index < len(target_lines):
        target_text = target_lines[index]
    else:
        target_text = "无对应标准文本"
    
    # 比较识别结果和标准文本
    if simplified_recognized_text == target_text:
        comparison_result = "匹配"
    else:
        comparison_result = "不匹配"
    
    # 添加到HTML表格中
    html_table += f"<tr><td>{relative_path}</td><td>{target_text}</td><td>{simplified_recognized_text}</td><td>{comparison_result}</td></tr>"

html_table += "</table>"

# 写入新的HTML文件
with open(comparison_file, 'w', encoding='utf-8') as file:
    file.write(html_table)

print(f"详细的比较结果已保存到 {comparison_file}")
