from opencc import OpenCC  # 用于简繁转换

# 初始化OpenCC进行繁体到简体的转换
cc = OpenCC('t2s')  # 使用繁体到简体转换器

# 结果保存文件
output_file = 'recognition_results.txt'
comparison_file = 'comparison_results.html'
standard_text_file = '../qldzj-ml/3.sutra-name-list.txt'


# 请额外处理以下三个文件，加上代码
# 038/468.png ，这个图片识别的结果是五经同卷，所以请加入五条五经同卷，同时从标准文本依次取5条文本与之对应。
# 038/492.png，同上处理，这个是六经同卷，因此取6条与之对应。
# 038/514.png，也是一样，这个是五经同卷，所以取5条。
# 请保留这三个图片的注释，因为每个特殊图片的情况都可能不一样。

# 特殊处理的文件路径
special_cases = {'020/329.png'}

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

# 遍历每一行识别结果
for result_line in recognition_results:
    parts = result_line.strip().split("：")
    relative_path = parts[0]
    recognized_text = parts[1] if len(parts) > 1 else ""

    # 检查是否为特殊处理的情况
    if relative_path in special_cases:
        simplified_recognized_text = cc.convert(recognized_text)
        html_table += (f"<tr>"
                       f"<td>{relative_path}</td>"
                       f"<td>无标准文本</td>"
                       f"<td>{recognized_text}</td>"
                       f"<td>{simplified_recognized_text}</td>"
                       f"<td>无需比较</td>"
                       f"</tr>")
        continue

    # 获取对应的目标文本
    while target_index < len(target_lines):
        target_text = target_lines[target_index]

        # 如果当前目标文本需要忽略，则跳过并继续下一个
        if target_text in ignore_texts:
            target_index += 1
            continue
        break

    # 如果所有目标文本都已处理完
    if target_index >= len(target_lines):
        target_text = "无对应标准文本"

    # 将识别结果转换为简体字
    simplified_recognized_text = cc.convert(recognized_text)

    # 比较识别结果和标准文本
    if target_text != "无对应标准文本":
        comparison_result = "匹配" if simplified_recognized_text == target_text else "不匹配"
    else:
        comparison_result = "无对应标准文本"

    # 添加到HTML表格中
    html_table += (f"<tr>"
                   f"<td>{relative_path}</td>"
                   f"<td>{target_text}</td>"
                   f"<td>{recognized_text}</td>"
                   f"<td>{simplified_recognized_text}</td>"
                   f"<td>{comparison_result}</td>"
                   f"</tr>")

    # 标准文本索引增加
    target_index += 1

html_table += "</table>"

# 写入新的HTML文件
with open(comparison_file, 'w', encoding='utf-8') as file:
    file.write(html_table)

print(f"详细的比较结果已保存到 {comparison_file}")
