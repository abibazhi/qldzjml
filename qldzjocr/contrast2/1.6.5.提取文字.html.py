import re

def parse_comparison_result(file_path):
    results = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            # 提取文件名（不包含路径）
            filename_match = re.match(r'\./selected_images/(.*?),', line)
            if not filename_match:
                continue  # 跳过无效行
            filename = filename_match.group(1)
            
            # 提取所有文本块中的文字
            text_match = re.search(r'所有文本块中的文字: (.*?)(?:\(|\|)', line)
            ocr_text = text_match.group(1).strip() if text_match else ''
            
            # 初始化默认值
            match_type = '未匹配'
            matched_text = ''
            row_number = 'N/A'
            match_length = 'N/A'
            
            # 尝试匹配全匹配
            full_match = re.search(r'全匹配: "([^"]+)" \(行号: (\d+)', line)
            if full_match:
                match_type = '全匹配'
                matched_text = full_match.group(1)
                row_number = full_match.group(2)
            else:
                # 尝试匹配部分匹配（包含匹配长度）
                partial_match = re.search(
                    r'部分匹配: "([^"]+)" \(行号: (\d+).*?匹配长度: (\d+)',
                    line,
                    re.DOTALL
                )
                if partial_match:
                    match_type = '部分匹配'
                    matched_text = partial_match.group(1)
                    row_number = partial_match.group(2)
                    match_length = partial_match.group(3)
            
            results.append({
                "文件名": filename,
                "所有文本块中的文字": ocr_text,
                "匹配类型": match_type,
                "匹配文字": matched_text,
                "行号": row_number,
                "匹配长度": match_length
            })
    return results

def generate_html_table(data):
    html = f"""
    <html>
    <head>
        <style>
            table {{
                border-collapse: collapse;
                width: 100%;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <table>
            <tr>
                <th>文件名</th>
                <th>所有文本块中的文字</th>
                <th>匹配类型</th>
                <th>匹配文字</th>
                <th>行号</th>
                <th>匹配长度</th>
            </tr>
    """
    
    for item in data:
        html += f"""
            <tr>
                <td>{item['文件名']}</td>
                <td>{item['所有文本块中的文字']}</td>
                <td>{item['匹配类型']}</td>
                <td>{item['匹配文字']}</td>
                <td>{item['行号']}</td>
                <td>{item['匹配长度']}</td>
            </tr>
        """
    
    html += """
        </table>
    </body>
    </html>
    """
    return html

def save_html_file(html_content, output_file="output.html"):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    input_file = "comparison_result_with_sliding_window.txt"  # 输入文件路径
    output_file = "output.html"  # 新增：定义 output_file 变量
    
    # 解析文件
    parsed_data = parse_comparison_result(input_file)
    
    # 生成HTML表格
    html_content = generate_html_table(parsed_data)
    
    # 保存为HTML文件，显式传递 output_file
    save_html_file(html_content, output_file)
    
    # 打印成功信息，使用定义好的 output_file
    print(f"HTML文件已保存至: {output_file}")
