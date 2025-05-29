import re

def parse_comparison_result(file_path):
    """
    解析比较结果文件，提取所需信息。
    :param file_path: 文件路径
    :return: 包含解析结果的列表，每个元素为字典格式。
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    results = []
    for line in lines:
        # 提取文件名
        filename_match = re.search(r"([^/]+\.png)", line)
        filename = filename_match.group(1) if filename_match else "未知文件名"

        # 提取所有文本块中的文字
        text_match = re.search(r", 所有文本块中的文字: (.*?) $", line)
        ocr_text = text_match.group(1) if text_match else ""

        # 初始化默认值
        match_type = "未匹配"
        matched_text = ""
        row_number = "N/A"

        # 查找匹配信息
        full_match = re.search(r"全匹配: \"(.*?)\" \(行号: (\d+)$", line)
        partial_match = re.search(r"部分匹配: \"(.*?)\" $行号: (\d+)$, 匹配部分: \"(.*?)\"", line)

        if full_match:
            match_type = "全匹配"
            matched_text = full_match.group(1)
            row_number = full_match.group(2)
        elif partial_match:
            match_type = "部分匹配"
            matched_text = partial_match.group(1)
            row_number = partial_match.group(2)

        # 添加到结果列表
        results.append({
            "filename": filename,
            "ocr_text": ocr_text,
            "match_type": match_type,
            "matched_text": matched_text,
            "row_number": row_number
        })

    return results

def print_results(results):
    """打印解析结果"""
    for result in results:
        print(f"文件名: {result['filename']}")
        print(f"所有文本块中的文字: {result['ocr_text']}")
        print(f"匹配类型: {result['match_type']}")
        print(f"匹配文字: {result['matched_text']}")
        print(f"行号: {result['row_number']}\n")

if __name__ == "__main__":
    input_file = "comparison_result_with_sliding_window.txt"  # 输入文件路径

    # 解析比较结果文件
    parsed_results = parse_comparison_result(input_file)

    # 打印解析结果
    print_results(parsed_results)
