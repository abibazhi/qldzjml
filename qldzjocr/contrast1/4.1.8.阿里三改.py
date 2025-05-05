import shutil
import os

def copy_file(src, dest):
    """复制文件"""
    shutil.copyfile(src, dest)

def read_lines(file_path):
    """读取文件内容为列表"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

def write_lines(file_path, lines):
    """写入内容到文件"""
    with open(file_path, 'w', encoding='utf-8') as file:
        for line in lines:
            file.write(f"{line}\n")

def find_matches(text_blocks, sutra_name, window_size):
    """查找指定大小的部分匹配项"""
    matches = []
    for text_block in text_blocks:
        for i in range(len(sutra_name) - window_size + 1):
            partial_name = sutra_name[i:i + window_size]
            if partial_name in text_block:
                matches.append((partial_name, window_size))
                break  # 找到一个匹配后跳出循环，避免重复匹配
    return matches

def compare_files_with_sliding_window_levels(sutra_list_file, extracted_info_file, output_file):
    # 复制被比较文本为结果文本
    copy_file(extracted_info_file, output_file)

    # 读取标准文本和被比较文本的内容
    sutra_lines = read_lines(sutra_list_file)
    result_lines = read_lines(output_file)

    matched_indices = set()  # 用于跟踪已经匹配过的行索引

    def update_result_line(line_idx, append_text):
        """更新结果文本中的指定行"""
        parts = result_lines[line_idx].split(", ", 1)
        result_lines[line_idx] = f"{parts[0]}, {parts[1]} {append_text}"

    # 全匹配阶段
    for sutra_idx, sutra_name in enumerate(sutra_lines):
        for idx, line in enumerate(result_lines):
            if idx in matched_indices: continue  # 跳过已经被匹配的行
            if sutra_name in line:
                matched_indices.add(idx)
                update_result_line(idx, f"(匹配到的标准文本: \"{sutra_name}\" (行号: {sutra_idx}))")
                break

    # 滑动窗口匹配阶段
    for window_size in range(10, 4, -1):  # 滑动窗口大小从10递减到5
        for sutra_idx, sutra_name in enumerate(sutra_lines):
            if any(sutra_name in result_lines[idx] for idx in matched_indices): continue  # 如果该行已经匹配过则跳过
            text_blocks = [line.split(", ", 1)[1] for idx, line in enumerate(result_lines) if idx not in matched_indices]
            matches = find_matches(text_blocks, sutra_name, window_size)
            for match_partial, match_length in matches:
                for idx, line in enumerate(result_lines):
                    if idx in matched_indices: continue
                    if match_partial in line.split(", ", 1)[1]:
                        matched_indices.add(idx)
                        update_result_line(idx, f"(匹配到的标准文本: \"{sutra_name}\" (行号: {sutra_idx}), 匹配部分: \"{match_partial}\", 匹配长度: {match_length})")
                        break

    # 写回结果文件
    write_lines(output_file, result_lines)

    # 统计匹配情况
    total_lines = len(result_lines)
    matched_count = len(matched_indices)
    match_percentage = (matched_count / total_lines) * 100
    print(f"匹配行数: {matched_count}/{total_lines} ({match_percentage:.2f}%)")
    print(f"已将比较结果保存到 {output_file}")

if __name__ == "__main__":
    sutra_list_file = "3.sutra-name-list.txt"  # 标准文件路径
    extracted_info_file = "extracted_file_path_and_all_text_blocks.txt"  # 提取信息文件路径
    output_file = "comparison_result_with_sliding_window_levels.txt"  # 输出文件路径

    compare_files_with_sliding_window_levels(sutra_list_file, extracted_info_file, output_file)
