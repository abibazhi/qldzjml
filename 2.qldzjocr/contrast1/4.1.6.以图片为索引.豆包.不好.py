def compare_files_with_sliding_window_levels(sutra_list_file, extracted_info_file, output_file):
    # 读取标准文件内容到列表中，同时记录每一行的行号
    sutra_names = []
    with open(sutra_list_file, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file.readlines(), 1):
            sutra_names.append((line_num, line.strip()))

    # 读取提取信息文件内容到字典中
    extracted_info = {}
    with open(extracted_info_file, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(", ", 1)
            if len(parts) == 2:
                file_path, text_block = parts
                extracted_info[text_block] = file_path

    # 以图片路径为键的字典，用于存储匹配信息
    image_path_matches = {path: [] for path in extracted_info.values()}

    def find_matches(sutra_name, line_num, window_size):
        """查找指定窗口大小的匹配项"""
        matches = []
        for i in range(len(sutra_name) - window_size + 1):
            partial_name = sutra_name[i:i + window_size]
            for text_block, file_path in extracted_info.items():
                if partial_name in text_block:
                    matches.append((file_path, line_num, partial_name, window_size))
        return matches

    # 滑动窗口大小从10递减到5
    for window_size in range(10, 2, -1):
        for line_num, sutra_name in sutra_names:
            matches = find_matches(sutra_name, line_num, window_size)
            for match in matches:
                file_path, matched_line_num, match_partial, match_length = match
                # 记录匹配信息
                image_path_matches[file_path].append((matched_line_num, sutra_name, match_length, match_partial))

    # 写入结果到输出文件
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for image_path, matches in image_path_matches.items():
            outfile.write(f"图片路径: {image_path}\n")
            if matches:
                for match in matches:
                    line_num, sutra_name, match_length, match_partial = match
                    outfile.write(f"    匹配到的标准文本: {sutra_name} (所在行数: {line_num})\n")
                    outfile.write(f"    匹配情况: 匹配了 {match_length} 个字，具体是: {match_partial}\n")
            else:
                outfile.write("    没有找到匹配的标准文本\n")
            outfile.write("-" * 50 + "\n")

    # 统计匹配情况并打印百分比
    total_images = len(image_path_matches)
    matched_images = sum(1 for matches in image_path_matches.values() if matches)
    match_percentage = (matched_images / total_images) * 100
    print(f"匹配图片数: {matched_images}/{total_images} ({match_percentage:.2f}%)")
    print(f"已将比较结果保存到 {output_file}")

if __name__ == "__main__":
    sutra_list_file = "3.sutra-name-list.txt"  # 标准文件路径
    extracted_info_file = "extracted_file_path_and_all_text_blocks.txt"  # 提取信息文件路径
    output_file = "comparison_result_with_sliding_window_levels.txt"  # 输出文件路径

    compare_files_with_sliding_window_levels(sutra_list_file, extracted_info_file, output_file)
