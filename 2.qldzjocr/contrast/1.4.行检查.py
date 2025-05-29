def read_file(file_path):
    """读取文件内容"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

def compare_files(sutra_list_path, image_text_path, output_html_path):
    """比较两个文件并输出结果到HTML文件"""
    sutras = read_file(sutra_list_path)
    images_texts = read_file(image_text_path)

    # 构建图像文本映射表
    image_dict = {}
    for line in images_texts:
        parts = line.split(", 文本: ")
        if len(parts) == 2:  # 确保分割得到两个部分
            img_path = parts[0]
            text = parts[1]
            image_dict[text] = img_path

    html_output = "<html><head><title>经文名称对比结果</title></head><body><h1>经文名称对比结果</h1><ul>"

    for sutra in sutras:
        if sutra in image_dict:
            html_output += f"<li>{sutra} - {image_dict[sutra]}</li>"
        else:
            html_output += f"<li>{sutra} - 没有找到</li>"

    html_output += "</ul></body></html>"

    # 将HTML结果保存到文件
    with open(output_html_path, 'w', encoding='utf-8') as output_file:
        output_file.write(html_output)

    print(f"HTML output has been saved to {output_html_path}")

# 设置文件路径
sutra_list_path = './3.sutra-name-list.txt'
image_text_path = './1.2.dark_background_files_simplified.txt'
output_html_path = './comparison_result.html'  # 输出HTML文件的位置

compare_files(sutra_list_path, image_text_path, output_html_path)
