def compare_files(sutra_list_file, extracted_info_file, output_file):
    # 读取标准文件内容到列表中
    with open(sutra_list_file, 'r', encoding='utf-8') as file:
        sutra_names = [line.strip() for line in file.readlines()]

    # 读取提取信息文件内容到字典中
    extracted_info = {}
    with open(extracted_info_file, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(", ", 1)
            if len(parts) == 2:
                file_path, text_block = parts
                extracted_info[text_block] = file_path

    # 比较并生成结果
    comparison_results = []
    for sutra_name in sutra_names:
        if sutra_name in extracted_info:
            comparison_results.append(f"{sutra_name}: {extracted_info[sutra_name]}")
        else:
            comparison_results.append(f"{sutra_name}: 没有找到")

    # 写入结果到输出文件
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for result in comparison_results:
            outfile.write(f"{result}\n")

if __name__ == "__main__":
    sutra_list_file = "3.sutra-name-list.txt"  # 标准文件路径
    extracted_info_file = "extracted_file_path_and_first_text_blocks.txt"  # 提取信息文件路径
    output_file = "comparison_result.txt"  # 输出文件路径
    
    compare_files(sutra_list_file, extracted_info_file, output_file)
    print(f"已将比较结果保存到 {output_file}")
