def extract_first_text_block(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    extracted_texts = []
    for line in lines:
        # 查找第一个文本块中的文字的位置
        start_idx = line.find("第一个文本块中的文字: ") + len("第一个文本块中的文字: ")
        end_idx = line.find(", 所有文本块中的文字:")
        
        if start_idx != -1 and end_idx != -1:
            first_text = line[start_idx:end_idx]
            extracted_texts.append(first_text)

    # 写入新的文件
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for text in extracted_texts:
            outfile.write(f"{text}\n")

if __name__ == "__main__":
    input_file_path = "detected_texts_output_simplified.txt"  # 输入文件路径
    output_file_path = "extracted_first_text_blocks.txt"  # 输出文件路径
    
    extract_first_text_block(input_file_path, output_file_path)
    print(f"已将第一个文本块中的文字提取并保存到 {output_file_path}")
