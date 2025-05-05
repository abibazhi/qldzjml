import os

def read_lines(file_path):
    """读取文件内容为列表"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

def write_lines(file_path, lines):
    """写入内容到文件"""
    with open(file_path, 'w', encoding='utf-8') as file:
        for line in lines:
            file.write(f"{line}\n")

def find_full_matches(ocr_lines, html_lines):
    """查找全匹配项"""
    full_matches = {}
    matched_ocr_indices = set()
    matched_html_indices = set()
    for ocr_idx, ocr_line in enumerate(ocr_lines):
        if ocr_idx in matched_ocr_indices:
            continue  # 跳过已经被匹配的行
        parts = ocr_line.split(' ', 1)
        ocr_text = parts[1] if len(parts) > 1 else ''
        for html_idx, html_line in enumerate(html_lines):
            if html_idx in matched_html_indices:
                continue  # 跳过已经被匹配的行
            if html_line in ocr_text:
                full_matches[ocr_idx] = (html_idx, html_line)
                matched_ocr_indices.add(ocr_idx)
                matched_html_indices.add(html_idx)
                break  # 找到匹配后跳出循环
    return full_matches, matched_ocr_indices, matched_html_indices

def find_partial_matches(ocr_lines, html_lines, matched_ocr_indices, matched_html_indices):
    """使用滑动窗口查找部分匹配项"""
    partial_matches = {}
    for window_size in range(10, 3, -1):  # 滑动窗口大小从10递减到5
        for ocr_idx, ocr_line in enumerate(ocr_lines):
            if ocr_idx in matched_ocr_indices or ocr_idx in partial_matches:
                continue  # 跳过已经匹配的行
            parts = ocr_line.split(' ', 1)
            ocr_text = parts[1] if len(parts) > 1 else ''
            for html_idx, html_line in enumerate(html_lines):
                if html_idx in matched_html_indices:
                    continue  # 跳过已经被匹配的行
                for i in range(len(html_line) - window_size + 1):
                    partial_text = html_line[i:i + window_size]
                    if partial_text in ocr_text:
                        partial_matches[ocr_idx] = (html_idx, html_line, partial_text, window_size)
                        matched_ocr_indices.add(ocr_idx)
                        matched_html_indices.add(html_idx)
                        break  # 找到匹配后跳出循环
                if ocr_idx in partial_matches:
                    break  # 找到匹配后跳出循环
    return partial_matches, matched_ocr_indices, matched_html_indices

def compare_files_with_sliding_window(ocr_file, html_file, output_file):
    # 读取两个文件的内容
    ocr_lines = read_lines(ocr_file)
    html_lines = read_lines(html_file)

    # 初始化结果列表
    result_lines = []

    # 全匹配阶段
    full_matches, matched_ocr_indices, matched_html_indices = find_full_matches(ocr_lines, html_lines)

    # 部分匹配阶段
    partial_matches, matched_ocr_indices, matched_html_indices = find_partial_matches(
        ocr_lines, html_lines, matched_ocr_indices, matched_html_indices
    )

    # 构建最终结果
    for ocr_idx, ocr_line in enumerate(ocr_lines):
        parts = ocr_line.split(' ', 1)
        filename = parts[0]
        ocr_text = parts[1] if len(parts) > 1 else ''

        if ocr_idx in full_matches:
            html_idx, html_line = full_matches[ocr_idx]
            result_lines.append(f"./selected_images/{filename}, {ocr_text} (全匹配: \"{html_line}\" (行号: {html_idx}))")
        elif ocr_idx in partial_matches:
            html_idx, html_line, partial_text, size = partial_matches[ocr_idx]
            result_lines.append(f"./selected_images/{filename}, {ocr_text} (部分匹配: \"{html_line}\" (行号: {html_idx}), 匹配部分: \"{partial_text}\", 匹配长度: {size})")
        else:
            result_lines.append(f"./selected_images/{filename}, {ocr_text} | 未匹配")

    # 写回结果文件
    write_lines(output_file, result_lines)

    print(f"比较完成，结果已保存到 {output_file}")

if __name__ == "__main__":
    ocr_file = "0.qldzj.ml.from.ocr.txt"  # OCR 文件路径
    html_file = "0.qldzj.ml.from.html.txt"  # HTML 文件路径
    output_file = "comparison_result_with_sliding_window.txt"  # 输出文件路径

    compare_files_with_sliding_window(ocr_file, html_file, output_file)
