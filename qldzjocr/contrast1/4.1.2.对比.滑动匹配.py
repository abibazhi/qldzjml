def compare_files_with_sliding_window_match(sutra_list_file, extracted_info_file, output_file):
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

    matched_paths = set()  # 用于跟踪已经匹配过的文件路径
    comparison_results = []

    def find_best_match(sutra_name):
        """查找最佳匹配，并返回匹配结果"""
        best_match = None
        window_size = 6
        for i in range(len(sutra_name) - window_size + 1):
            partial_name = sutra_name[i:i + window_size]
            for text_block, file_path in extracted_info.items():
                if partial_name in text_block and file_path not in matched_paths:
                    best_match = file_path
                    matched_paths.add(file_path)
                    return best_match, partial_name
        return None, None

    total_lines = len(sutra_names)
    matched_count = 0

    for sutra_name in sutra_names:
        match_path, match_partial = find_best_match(sutra_name)
        if match_path:
            matched_count += 1
            comparison_results.append(f"{sutra_name}: {match_path} (匹配部分: {match_partial})")
        else:
            comparison_results.append(f"{sutra_name}: 没有找到")

    # 写入结果到输出文件
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for result in comparison_results:
            outfile.write(f"{result}\n")

    # 打印匹配行数和总行数的百分比
    match_percentage = (matched_count / total_lines) * 100
    print(f"匹配行数: {matched_count}/{total_lines} ({match_percentage:.2f}%)")

if __name__ == "__main__":
    sutra_list_file = "3.sutra-name-list.txt"  # 标准文件路径
    extracted_info_file = "extracted_file_path_and_first_text_blocks.txt"  # 提取信息文件路径
    output_file = "comparison_result_with_sliding_window_match.txt"  # 输出文件路径
    
    compare_files_with_sliding_window_match(sutra_list_file, extracted_info_file, output_file)
    print(f"已将比较结果保存到 {output_file}")
