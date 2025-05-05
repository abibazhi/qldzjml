import opencc

# 初始化OpenCC用于繁体转简体
cc = opencc.OpenCC('t2s')

def read_file(file_path):
    """读取文件内容"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

def compare_files(sutra_list_path, image_text_path, output_html_path):
    """比较两个文件并输出结果到HTML文件"""
    sutras = read_file(sutra_list_path)
    images_texts = read_file(image_text_path)

    # 解析第二个文件内容
    image_dict = {}
    for line in images_texts:
        parts = line.strip().split(", ")
        img_path = parts[0]
        text = cc.convert(parts[1][5:])  # 转换为简体并去掉前缀"文本: "
        image_dict[text] = img_path

    html_output = "<html><head><title>经文名称对比结果</title></head><body><h1>经文名称对比结果</h1><ul>"

    for sutra in sutras:
        sutra_simplified = cc.convert(sutra.strip())
        if sutra_simplified in image_dict:
            html_output += f"<li>{sutra_simplified} - {image_dict[sutra_simplified]}</li>"
        else:
            html_output += f"<li>{sutra_simplified} - 没有找到</li>"

    html_output += "</ul></body></html>"

    # 将HTML结果保存到文件
    with open(output_html_path, 'w', encoding='utf-8') as output_file:
        output_file.write(html_output)

    print(f"HTML output has been saved to {output_html_path}")

# 设置文件路径
sutra_list_path = '/home/jm/dev/qldzjocr/ml/3.sutra-name-list.txt'
image_text_path = '/mnt/d/temp/temp_images/dark_background_files.txt'
output_html_path = './comparison_result.html'  # 输出HTML文件的位置

compare_files(sutra_list_path, image_text_path, output_html_path)
