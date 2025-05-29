import re

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
            
            # 4. 整合数据
            result = {
                "文件名": filename,
                "所有文本块中的文字": text_block,
                **match_info
            }
            results.append(result)
    return results

def generate_html_table(data):
    html = """
    <html>
    <head>
        <title>OCR Comparison Results</title>
        <style>
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; }
            th { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <table>
            <tr>
                <th>文件名</th>
                <th>所有文本块中的文字</th>
                <th>匹配类型</th>
                <th>匹配内容</th>
                <th>行号</th>
                <th>匹配部分</th>
                <th>匹配长度/字符数</th>
            </tr>
    """
    
    for item in data:
        html += "<tr>"
        html += f"<td>{item.get('文件名', '')}</td>"
        html += f"<td>{item.get('所有文本块中的文字', '')}</td>"
        html += f"<td>{item.get('匹配类型', '')}</td>"
        html += f"<td>{item.get('匹配内容', '')}</td>"
        html += f"<td>{item.get('行号', '')}</td>"
        html += f"<td>{item.get('匹配部分', '')}</td>"
        html += f"<td>{item.get('匹配长度', item.get('匹配字符数', ''))}</td>"
        html += "</tr>"
    
    html += """
        </table>
    </body>
    </html>
    """
    return html

# 执行解析并生成HTML
data = parse_comparison_result("comparison_result_with_author.txt")
html_content = generate_html_table(data)

# 保存为HTML文件
with open("comparison_results.html", "w", encoding="utf-8") as f:
    f.write(html_content)
