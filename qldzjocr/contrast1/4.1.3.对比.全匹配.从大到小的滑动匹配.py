def compare_files_with_sliding_window_levels(sutra_list_file, extracted_info_file, output_file):
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
    comparison_results = {sutra_name: "没有找到" for sutra_name in sutra_names}

    def find_matches(sutra_name, window_size):
        """查找指定窗口大小的匹配项"""
        matches = []
        for i in range(len(sutra_name) - window_size + 1):
            partial_name = sutra_name[i:i + window_size]
            for text_block, file_path in extracted_info.items():
                if partial_name in text_block and file_path not in matched_paths:
                    matches.append((file_path, partial_name, window_size))
        return matches

    # 滑动窗口大小从10递减到5
    for window_size in range(10, 2, -1):
        for sutra_name in sutra_names:
            if comparison_results[sutra_name] == "没有找到":
                matches = find_matches(sutra_name, window_size)
                if matches:
                    match_path, match_partial, match_length = matches[0]  # 取第一个匹配结果
                    matched_paths.add(match_path)
                    comparison_results[sutra_name] = f"{match_path} (部分匹配长度: {match_length}, 匹配部分: {match_partial})"

    # 写入结果到输出文件
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for sutra_name, result in comparison_results.items():
            outfile.write(f"{sutra_name}: {result}\n")

    # 统计匹配情况并打印百分比
    total_lines = len(sutra_names)
    matched_count = sum(1 for result in comparison_results.values() if result != "没有找到")
    match_percentage = (matched_count / total_lines) * 100
    print(f"匹配行数: {matched_count}/{total_lines} ({match_percentage:.2f}%)")
    print(f"已将比较结果保存到 {output_file}")

if __name__ == "__main__":
    sutra_list_file = "3.sutra-name-list.txt"  # 标准文件路径
    extracted_info_file = "extracted_file_path_and_first_text_blocks.txt"  # 提取信息文件路径
    output_file = "comparison_result_with_sliding_window_levels.txt"  # 输出文件路径
    
    compare_files_with_sliding_window_levels(sutra_list_file, extracted_info_file, output_file)
