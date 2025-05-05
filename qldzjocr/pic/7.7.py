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
    '038/008.png': 2,      # 二经同卷
    '038/234.png': 4,      # 四经同卷
    '038/294.png': 2,      # 二经同卷
    '038/310.png': 3,      # 三经同卷
    '038/468.png': 5,      # 五经同卷
    '038/492.png': 6,      # 六经同卷
    '038/514.png': 5,      # 五经同卷
    '038/566.png': 4,      # 四经同卷
    '038/602.png': 2,      # 二经同卷
    '038/620.png': 2,      # 二经同卷
    '038/638.png': 2,      # 二经同卷
    '039/149.png': 4,      # 四经同卷
    '039/363.png': 4,      # 四经同卷
    '039/383.png': 5,      # 五经同卷
    '039/407.png': 2,       # 二经同卷
    '039/423.png': 4,       # 二经同卷
    '039/443.png': 3,       # 二经同卷
    '039/459.png': 3,       # 二经同卷
    '039/475.png': 3,       # 二经同卷
    '039/495.png': 4,       # 二经同卷
    '039/537.png': 8,       # 八经同卷
    '039/561.png': 8,       # 八经同卷
    '039/757.png': 2,       # 二经同卷
    '039/773.png': 2,       # 二经同卷
    '040/673.png': 3,       # 三经同卷
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

# 辅助函数：添加一行到HTML表格
def add_to_html_table(relative_path, merged_recognized_text, target_text, target_index):
    simplified_merged_text = cc.convert(merged_recognized_text.strip())
    
    if target_text != "无对应标准文本":
        comparison_result = "匹配" if simplified_merged_text == target_text else "不匹配"
    else:
        comparison_result = "无对应标准文本"

    row = (f"<tr>"
           f"<td>{relative_path}</td>"
           f"<td>{target_text}</td>"
           f"<td>{merged_recognized_text.strip()}</td>"
           f"<td>{simplified_merged_text}</td>"
           f"<td>{comparison_result}</td>"
           f"</tr>")
    return row, target_index + 1 if target_text != "无对应标准文本" else target_index

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
        if current_image:
            if current_image in special_cases.keys():
                if current_image.startswith('020'):  # 处理020/329.png的情况
                    html_table += (f"<tr>"
                                   f"<td>{current_image}</td>"
                                   f"<td>无标准文本</td>"
                                   f"<td>{merged_recognized_text.strip()}</td>"
                                   f"<td>{cc.convert(merged_recognized_text.strip())}</td>"
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
                                   f"<td>{cc.convert(merged_recognized_text.strip())}</td>"
                                   f"<td>{comparison_result}</td>"
                                   f"</tr>")

                    target_index += num_entries
            else:
                # 正常处理非特殊图片
                while target_index < len(target_lines):
                    target_text = target_lines[target_index]

                    # 如果当前目标文本需要忽略，则跳过并继续下一个
                    if target_text in ignore_texts:
                        target_index += 1
                        continue
                    break

                if target_index >= len(target_lines):
                    target_text = "无对应标准文本"

                row, target_index = add_to_html_table(current_image, merged_recognized_text, target_text, target_index)
                html_table += row

        # 更新当前图片和初始化合并文本
        current_image = relative_path
        merged_recognized_text = recognized_text + "\n"

# 处理最后一个图片的结果
if current_image:
    if current_image in special_cases.keys():
        if current_image.startswith('020'):  # 处理020/329.png的情况
            html_table += (f"<tr>"
                           f"<td>{current_image}</td>"
                           f"<td>无标准文本</td>"
                           f"<td>{merged_recognized_text.strip()}</td>"
                           f"<td>{cc.convert(merged_recognized_text.strip())}</td>"
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
                           f"<td>{cc.convert(merged_recognized_text.strip())}</td>"
                           f"<td>{comparison_result}</td>"
                           f"</tr>")

            target_index += num_entries
    else:
        # 正常处理非特殊图片
        while target_index < len(target_lines):
            target_text = target_lines[target_index]

            # 如果当前目标文本需要忽略，则跳过并继续下一个
            if target_text in ignore_texts:
                target_index += 1
                continue
            break

        if target_index >= len(target_lines):
            target_text = "无对应标准文本"

        row, target_index = add_to_html_table(current_image, merged_recognized_text, target_text, target_index)
        html_table += row

html_table += "</table>"

# 写入新的HTML文件
with open(comparison_file, 'w', encoding='utf-8') as file:
    file.write(html_table)

print(f"详细的比较结果已保存到 {comparison_file}")
