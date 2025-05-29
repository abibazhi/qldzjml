import re

def parse_comparison_result(file_path):
    results = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            # 1. 提取文件名（仅文件名部分）
            filename = re.match(r'\./selected_images/(qldzjpng_\d+_\d+\.png)', line).group(1)
            
            # 2. 提取所有文本块中的文字（逗号后到第一个 ( 或 |）
            text_block = re.search(r',\s*(.*?)(?=\s*\(|\s*\|)', line).group(1).strip()
            
            # 3. 解析匹配类型（全匹配/部分匹配/模糊匹配）
            match_info = {}
            full_match = re.search(r'\(全匹配: "(.*?)" 行号: (\d+)', line)
            partial_match = re.search(r'\(部分匹配: "(.*?)" 行号: (\d+).*?匹配部分: "(.*?)".*?(?:窗口大小|匹配长度): (\d+)', line)
            fuzzy_match = re.search(r'\(模糊匹配: "(.*?)" 行号: (\d+).*?匹配字符数: (\d+)', line)
            
            if full_match:
                match_info = {
                    "匹配类型": "全匹配",
                    "匹配内容": full_match.group(1),
                    "行号": full_match.group(2)
                }
            elif partial_match:
                match_info = {
                    "匹配类型": "部分匹配",
                    "匹配内容": partial_match.group(1),
                    "行号": partial_match.group(2),
                    "匹配部分": partial_match.group(3),
                    "匹配长度": partial_match.group(4)
                }
            elif fuzzy_match:
                match_info = {
                    "匹配类型": "模糊匹配",
                    "匹配内容": fuzzy_match.group(1),
                    "行号": fuzzy_match.group(2),
                    "匹配字符数": fuzzy_match.group(3)
                }
            else:
                match_info = {
                    "匹配类型": "未匹配"
                }
            
            # 4. 整合数据到结果列表
            results.append({
                "文件名": filename,
                "所有文本块中的文字": text_block,
                **match_info  # 合并匹配信息
            })
    return results

# 示例使用
data = parse_comparison_result("comparison_result_with_author.txt")
for item in data:
    print(item)
