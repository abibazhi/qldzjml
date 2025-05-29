def compare_files_with_partial_match(sutra_list_file, extracted_info_file, output_file):
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
        """查找最佳匹配，并返回匹配结果和匹配程度"""
        best_match = None
        best_match_length = 0
        for i in range(len(sutra_name), 5, -1):  # 直到字符串长度为6
            partial_name = sutra_name[:i]
            for text_block, file_path in extracted_info.items():
                if text_block.startswith(partial_name) and file_path not in matched_paths:
                    if i > best_match_length:
                        best_match = file_path
                        best_match_length = i
        return best_match, best_match_length

    for sutra_name in sutra_names:
        match_path, match_length = find_best_match(sutra_name)
        if match_path:
            matched_paths.add(match_path)
            comparison_results.append(f"{sutra_name}: {match_path} (部分匹配长度: {match_length})")
        else:
            comparison_results.append(f"{sutra_name}: 没有找到")

    # 写入结果到输出文件
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for result in comparison_results:
            outfile.write(f"{result}\n")

if __name__ == "__main__":
    sutra_list_file = "3.sutra-name-list.txt"  # 标准文件路径
    extracted_info_file = "extracted_file_path_and_first_text_blocks.txt"  # 提取信息文件路径
    output_file = "comparison_result_with_partial_match.txt"  # 输出文件路径
    
    compare_files_with_partial_match(sutra_list_file, extracted_info_file, output_file)
    print(f"已将比较结果保存到 {output_file}")
