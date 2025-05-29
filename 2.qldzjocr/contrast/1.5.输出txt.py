def read_file(file_path):
    """读取文件内容"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

def compare_files(sutra_list_path, image_text_path, output_txt_path):
    """比较两个文件并输出结果到TXT文件"""
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

    txt_output = ""

    for sutra in sutras:
        if sutra in image_dict:
            txt_output += f"{sutra} - {image_dict[sutra]}\n"
        else:
            txt_output += f"{sutra} - 没有找到\n"

    # 将TXT结果保存到文件
    with open(output_txt_path, 'w', encoding='utf-8') as output_file:
        output_file.write(txt_output)

    print(f"TXT output has been saved to {output_txt_path}")

# 设置文件路径
sutra_list_path = './3.sutra-name-list.txt'
image_text_path = './1.2.dark_background_files_simplified.txt'
output_txt_path = './comparison_result.txt'  # 输出TXT文件的位置

compare_files(sutra_list_path, image_text_path, output_txt_path)
