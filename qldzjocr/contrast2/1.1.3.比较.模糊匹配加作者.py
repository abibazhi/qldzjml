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
    """查找全匹配项（仅使用经名部分）"""
    full_matches = {}
    matched_ocr_indices = set()
    matched_html_indices = set()
    for ocr_idx, ocr_line in enumerate(ocr_lines):
        if ocr_idx in matched_ocr_indices:
            continue
        parts = ocr_line.split(' ', 1)
        ocr_text = parts[1] if len(parts) > 1 else ''
        for html_idx, html_line in enumerate(html_lines):
            if html_idx in matched_html_indices:
                continue
            # 取经名部分（经名和作者用逗号分隔）
            html_name = html_line.split(',', 1)[0].strip()
            if html_name in ocr_text:
                full_matches[ocr_idx] = (html_idx, html_line)  # 保存完整行（含作者）
                matched_ocr_indices.add(ocr_idx)
                matched_html_indices.add(html_idx)
                break
    return full_matches, matched_ocr_indices, matched_html_indices

def find_partial_matches(ocr_lines, html_lines, matched_ocr_indices, matched_html_indices):
    """滑动窗口部分匹配（仅使用经名部分）"""
    partial_matches = {}
    for window_size in range(10, 1, -1):  # 窗口大小从10递减到4
        for ocr_idx, ocr_line in enumerate(ocr_lines):
            if ocr_idx in matched_ocr_indices or ocr_idx in partial_matches:
                continue
            parts = ocr_line.split(' ', 1)
            ocr_text = parts[1] if len(parts) > 1 else ''
            for html_idx, html_line in enumerate(html_lines):
                if html_idx in matched_html_indices:
                    continue
                html_name = html_line.split(',', 1)[0].strip()  # 取经名部分
                if len(html_name) < window_size:
                    continue
                for i in range(len(html_name) - window_size + 1):
                    partial_text = html_name[i:i + window_size]
                    if partial_text in ocr_text:
                        partial_matches[ocr_idx] = (html_idx, html_line, partial_text, window_size)
                        matched_ocr_indices.add(ocr_idx)
                        matched_html_indices.add(html_idx)
                        break
                if ocr_idx in partial_matches:
                    break
    return partial_matches, matched_ocr_indices, matched_html_indices

def find_fuzzy_matches(ocr_lines, html_lines, matched_ocr_indices, matched_html_indices):
    """模糊匹配（使用整行数据，包括作者）"""
    fuzzy_matches = {}
    for ocr_idx in range(len(ocr_lines)):
        if ocr_idx in matched_ocr_indices:
            continue
        ocr_line = ocr_lines[ocr_idx]
        for html_idx in range(len(html_lines)):
            if html_idx in matched_html_indices:
                continue
            html_line = html_lines[html_idx]
            # 使用整行进行模糊匹配
            match_count = 0
            ocr_pos = 0
            for c in html_line:
                found_pos = ocr_line.find(c, ocr_pos)
                if found_pos != -1:
                    match_count += 1
                    ocr_pos = found_pos + 1
                else:
                    break
            if match_count >= 4:  # 匹配至少4个字符
                fuzzy_matches[ocr_idx] = (html_idx, html_line, match_count)
                matched_ocr_indices.add(ocr_idx)
                matched_html_indices.add(html_idx)
                break
    return fuzzy_matches, matched_ocr_indices, matched_html_indices

def compare_files_with_sliding_window(ocr_file, html_file, output_file):
    # 读取文件内容
    ocr_lines = read_lines(ocr_file)
    html_lines = read_lines(html_file)
    
    result_lines = []
    
    # 全匹配阶段
    full_matches, matched_ocr_indices, matched_html_indices = find_full_matches(ocr_lines, html_lines)
    
    # 部分匹配阶段
    partial_matches, matched_ocr_indices, matched_html_indices = find_partial_matches(
        ocr_lines, html_lines, matched_ocr_indices, matched_html_indices
    )
    
    # 模糊匹配阶段
    fuzzy_matches, matched_ocr_indices, matched_html_indices = find_fuzzy_matches(
        ocr_lines, html_lines, matched_ocr_indices, matched_html_indices
    )
    
    # 构建结果
    for ocr_idx, ocr_line in enumerate(ocr_lines):
        parts = ocr_line.split(' ', 1)
        filename = parts[0]
        ocr_text = parts[1] if len(parts) > 1 else ''
        
        if ocr_idx in full_matches:
            html_idx, html_line = full_matches[ocr_idx]
            result_lines.append(
                f"./selected_images/{filename}, {ocr_text} (全匹配: \"{html_line}\" 行号: {html_idx})"
            )
        elif ocr_idx in partial_matches:
            html_idx, html_line, partial_text, size = partial_matches[ocr_idx]
            result_lines.append(
                f"./selected_images/{filename}, {ocr_text} (部分匹配: \"{html_line}\" 行号: {html_idx}, 匹配部分: \"{partial_text}\", 窗口大小: {size})"
            )
        elif ocr_idx in fuzzy_matches:
            html_idx, html_line, match_count = fuzzy_matches[ocr_idx]
            result_lines.append(
                f"./selected_images/{filename}, {ocr_text} (模糊匹配: \"{html_line}\" 行号: {html_idx}, 匹配字符数: {match_count})"
            )
        else:
            result_lines.append(f"./selected_images/{filename}, {ocr_text} | 未匹配")
    
    # 写入结果
    write_lines(output_file, result_lines)
    print(f"匹配完成，结果已保存至 {output_file}")

if __name__ == "__main__":
    ocr_file = "0.qldzj.ml.from.ocr.txt"  # OCR文件路径
    html_file = "0.qldzj.ml.from.html.add.author.txt"  # 新的HTML文件（含作者）
    output_file = "comparison_result_with_author.txt"  # 输出文件
    
    compare_files_with_sliding_window(ocr_file, html_file, output_file)
