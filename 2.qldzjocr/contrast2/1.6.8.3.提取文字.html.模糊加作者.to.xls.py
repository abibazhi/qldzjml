import re
import pandas as pd

def parse_comparison_result(file_path):
    results = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            # 1. 提取文件名
            filename_match = re.match(r'\./selected_images/(qldzjpng_\d+_\d+\.png)', line)
            if not filename_match:
                continue
            filename = filename_match.group(1)
            
            # 2. 提取文本块内容（去除前缀）
            text_block_match = re.search(r'所有文本块中的文字:\s*(.*?)(?=\s*\(|\s*\|)', line)
            text_block = text_block_match.group(1).strip() if text_block_match else ''
            
            # 3. 解析匹配信息
            match_info = {}
            full_match = re.search(r'\(全匹配: "(.*?)" 行号: (\d+)', line)
            partial_match = re.search(
                r'\(部分匹配: "(.*?)" 行号: (\d+).*?匹配部分: "(.*?)".*?(?:窗口大小|匹配长度): (\d+)',
                line
            )
            fuzzy_match = re.search(
                r'\(模糊匹配: "(.*?)" 行号: (\d+).*?匹配字符数: (\d+)',
                line
            )
            
            if full_match:
                match_info = {
                    "匹配类型": "全匹配",
                    "匹配内容": full_match.group(1),
                    "行号": full_match.group(2),
                    "匹配部分": "",
                    "匹配长度/字符数": ""
                }
            elif partial_match:
                match_info = {
                    "匹配类型": "部分匹配",
                    "匹配内容": partial_match.group(1),
                    "行号": partial_match.group(2),
                    "匹配部分": partial_match.group(3),
                    "匹配长度/字符数": partial_match.group(4)
                }
            elif fuzzy_match:
                match_info = {
                    "匹配类型": "模糊匹配",
                    "匹配内容": fuzzy_match.group(1),
                    "行号": fuzzy_match.group(2),
                    "匹配部分": "",
                    "匹配长度/字符数": fuzzy_match.group(3)
                }
            else:
                match_info = {
                    "匹配类型": "未匹配",
                    "匹配内容": "",
                    "行号": "",
                    "匹配部分": "",
                    "匹配长度/字符数": ""
                }
            
            # 4. 整合数据
            result = {
                "文件名": filename,
                "所有文本块中的文字": text_block,
                **match_info
            }
            results.append(result)
    return results

def save_to_excel(data, output_path):
    # 创建DataFrame并填充数据
    df = pd.DataFrame(data)
    # 重置列顺序（确保列名正确）
    columns = [
        "文件名",
        "所有文本块中的文字",
        "匹配类型",
        "匹配内容",
        "行号",
        "匹配部分",
        "匹配长度/字符数"
    ]
    df = df[columns]
    
    # 导出为Excel
    df.to_excel(output_path, index=False, engine='openpyxl')

# 执行解析并保存为Excel
data = parse_comparison_result("comparison_result_with_author.txt")
save_to_excel(data, "comparison_results.xlsx")

print("Excel文件已生成：comparison_results.xlsx")
