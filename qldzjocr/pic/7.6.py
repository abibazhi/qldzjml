from opencc import OpenCC  # 用于简繁转换

# 初始化OpenCC进行繁体到简体的转换
cc = OpenCC('t2s')  # 使用繁体到简体转换器

# 结果保存文件
output_file = 'recognition_results.txt'
comparison_file = 'comparison_results.html'
standard_text_file = '../qldzj-ml/3.sutra-name-list.txt'

# 特殊处理的文件及其对应的标准文本条目数或特殊处理标志
special_cases = {
    '020/329.png': None,   # 原有的特殊处理情况，不需要从标准文本取条目
    '038/468.png': 5,      # 五经同卷
    '038/492.png': 6,      # 六经同卷
    '038/514.png': 5,      # 五经同卷
    '039/149.png': 4,      # 四经同卷
    '039/363.png': 4       # 四经同卷（新增）
}

# 标准文本中需要忽略的条目
ignore_texts = {"大方广佛华严经普贤菩萨行愿品"}

# 读取标准文本内容
with open(standard_text_file, 'r', encoding='utf-8') as file:
    target_lines = file.read().splitlines()

# 读取recognition_results.txt内容
with open(output_file, 'r', encoding='utf-8') as file:
    recognition_results = file.readlines()

# 创建HTML表格
html_table = ("<table border='1'>"
              "<tr><th>相对目录</th><th>目标文本</th><th>识别文本（原始）</th><th>识别文本（简体）</th><th>比较结果</th></tr>")

# 初始化标准文本的索引
target_index = 0

# 遍历每一行识别结果，并合并同一图片的结果
current_image = ''
merged_recognized_text = ''

for result_line in recognition_results:
    parts = result_line.strip().split("：")
    relative_path = parts[0]
    recognized_text = parts[1] if len(parts) > 1 else ""

    # 如果当前行属于同一个图片，则合并识别文本
    if current_image == relative_path:
        merged_recognized_text += recognized_text + "\n"
    else:
        # 处理上一个图片的结果（如果不是第一个图片）
        if current_image and current_image in special_cases.keys():
            simplified_merged_text = cc.convert(merged_recognized_text.strip())
            
            if current_image.startswith('020'):  # 处理020/329.png的情况
                html_table += (f"<tr>"
                               f"<td>{current_image}</td>"
                               f"<td>无标准文本</td>"
                               f"<td>{merged_recognized_text.strip()}</td>"
                               f"<td>{simplified_merged_text}</td>"
                               f"<td>无需比较</td>"
                               f"</tr>")
            elif current_image.startswith(('038', '039')):  # 处理038和039目录下的特殊情况
                num_entries = special_cases[current_image]
                target_text = '<br>'.join(target_lines[target_index:target_index + num_entries])
                comparison_result = "无需比较"  # 对于特殊处理情况，默认设置为无需比较

                html_table += (f"<tr>"
                               f"<td>{current_image}</td>"
                               f"<td>{target_text}</td>"
                               f"<td>{merged_recognized_text.strip()}</td>"
                               f"<td>{simplified_merged_text}</td>"
                               f"<td>{comparison_result}</td>"
                               f"</tr>")

                # 更新标准文本索引
                target_index += num_entries
        
        # 更新当前图片和初始化合并文本
        current_image = relative_path
        merged_recognized_text = recognized_text + "\n"

# 处理最后一个图片的结果
if current_image in special_cases.keys():
    simplified_merged_text = cc.convert(merged_recognized_text.strip())

    if current_image.startswith('020'):  # 处理020/329.png的情况
        html_table += (f"<tr>"
                       f"<td>{current_image}</td>"
                       f"<td>无标准文本</td>"
                       f"<td>{merged_recognized_text.strip()}</td>"
                       f"<td>{simplified_merged_text}</td>"
                       f"<td>无需比较</td>"
                       f"</tr>")
    elif current_image.startswith(('038', '039')):  # 处理038和039目录下的特殊情况
        num_entries = special_cases[current_image]
        target_text = '<br>'.join(target_lines[target_index:target_index + num_entries])
        comparison_result = "无需比较"  # 对于特殊处理情况，默认设置为无需比较

        html_table += (f"<tr>"
                       f"<td>{current_image}</td>"
                       f"<td>{target_text}</td>"
                       f"<td>{merged_recognized_text.strip()}</td>"
                       f"<td>{simplified_merged_text}</td>"
                       f"<td>{comparison_result}</td>"
                       f"</tr>")

        # 更新标准文本索引
        target_index += num_entries

html_table += "</table>"

# 写入新的HTML文件
with open(comparison_file, 'w', encoding='utf-8') as file:
    file.write(html_table)

print(f"详细的比较结果已保存到 {comparison_file}")
