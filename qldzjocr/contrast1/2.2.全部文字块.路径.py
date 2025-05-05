def extract_file_path_and_all_text_blocks(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    extracted_info = []
    for line in lines:
        # 查找文件路径的位置
        file_path_start_idx = line.find("图片路径: ") + len("图片路径: ")
        file_path_end_idx = line.find(", 所有文本块中的文字:")
        file_path = line[file_path_start_idx:file_path_end_idx]

        # 查找所有文本块中的文字的位置
        text_start_idx = line.find("所有文本块中的文字: ") + len("所有文本块中的文字: ")
        
        all_texts = line[text_start_idx:].strip()  # 获取所有文本块中的文字，并去掉前后空格

        if all_texts:  # 如果找到了文本
            extracted_info.append((file_path, all_texts))

    # 写入新的文件
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for file_path, all_texts in extracted_info:
            outfile.write(f"{file_path}, {all_texts}\n")

if __name__ == "__main__":
    input_file_path = "detected_texts_output_simplified.txt"  # 输入文件路径
    output_file_path = "extracted_file_path_and_all_text_blocks.txt"  # 输出文件路径

    extract_file_path_and_all_text_blocks(input_file_path, output_file_path)
    print(f"已将文件路径和所有文本块中的文字提取并保存到 {output_file_path}")
