import re

def parse_comparison_result(file_path):
    results = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            # 提取文件名（不包含路径）
            filename = re.match(r'\./selected_images/(.*?),', line).group(1)
            
            # 提取所有文本块中的文字
            text_match = re.search(r'所有文本块中的文字: (.*?)(?:$|\|)', line)
            ocr_text = text_match.group(1).strip() if text_match else ''
            
            # 判断匹配类型
            if '全匹配' in line:
                match_type = '全匹配'
                # 提取匹配的文本和行号
                match_info = re.search(r'全匹配: "(.*?)" \(行号: (\d+)$', line)
                matched_text = match_info.group(1)
                row_number = match_info.group(2)
            elif '部分匹配' in line:
                match_type = '部分匹配'
                # 提取匹配的文本和行号
                match_info = re.search(r'部分匹配: "(.*?)" $行号: (\d+)$', line)
                matched_text = match_info.group(1)
                row_number = match_info.group(2)
            else:
                match_type = '未匹配'
                matched_text = ''
                row_number = 'N/A'
            
            results.append({
                "文件名": filename,
                "所有文本块中的文字": ocr_text,
                "匹配类型": match_type,
                "匹配文字": matched_text,
                "行号": row_number
            })
    return results

def print_results(results):
    for result in results:
        print(f"文件名: {result['文件名']}")
        print(f"所有文本块中的文字: {result['所有文本块中的文字']}")
        print(f"匹配类型: {result['匹配类型']}")
        print(f"匹配文字: {result['匹配文字']}")
        print(f"行号: {result['行号']}")
        print('-' * 40)

if __name__ == "__main__":
    input_file = "comparison_result_with_sliding_window.txt"  # 输入文件路径
    
    # 解析文件
    parsed_data = parse_comparison_result(input_file)
    
    # 打印结果
    print_results(parsed_data)
