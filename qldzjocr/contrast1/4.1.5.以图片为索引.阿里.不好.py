def compare_files_with_sliding_window_levels(sutra_list_file, extracted_info_file, output_file):
    # 读取标准文件内容到列表中
    with open(sutra_list_file, 'r', encoding='utf-8') as file:
        sutra_lines = [(line.strip(), idx) for idx, line in enumerate(file.readlines())]

    # 读取提取信息文件内容到字典中
    extracted_info = {}
    with open(extracted_info_file, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(", ", 1)
            if len(parts) == 2:
                file_path, text_block = parts
                if file_path not in extracted_info:
                    extracted_info[file_path] = []
                extracted_info[file_path].append(text_block)

    comparison_results = {file_path: [] for file_path in extracted_info.keys()}

    def find_matches(text_block, sutra_name, sutra_line_number):
        """查找指定文本块与经文名称之间的匹配项"""
        matches = []
        for window_size in range(10, 2, -1):  # 滑动窗口大小从10递减到3
            for i in range(len(sutra_name) - window_size + 1):
                partial_name = sutra_name[i:i + window_size]
                if partial_name in text_block:
                    matches.append((partial_name, window_size, sutra_line_number))
                    break  # 找到一个匹配后跳出循环，避免重复匹配
        return matches

    for file_path, text_blocks in extracted_info.items():
        for text_block in text_blocks:
            for sutra_name, sutra_line_number in sutra_lines:
                matches = find_matches(text_block, sutra_name, sutra_line_number)
                if matches:
                    comparison_results[file_path].extend(matches)

    # 写入结果到输出文件
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for file_path, matches in comparison_results.items():
            if matches:
                outfile.write(f"{file_path}:\n")
                for match_partial, match_length, sutra_line_number in matches:
                    outfile.write(f"  匹配到的标准文本行号: {sutra_line_number}, 匹配部分: {match_partial}, 匹配长度: {match_length}\n")
            else:
                outfile.write(f"{file_path}: 没有找到匹配\n")

    print(f"已将比较结果保存到 {output_file}")

if __name__ == "__main__":
    sutra_list_file = "3.sutra-name-list.txt"  # 标准文件路径
    extracted_info_file = "extracted_file_path_and_all_text_blocks.txt"  # 提取信息文件路径
    output_file = "comparison_result_with_sliding_window_levels.txt"  # 输出文件路径

    compare_files_with_sliding_window_levels(sutra_list_file, extracted_info_file, output_file)
