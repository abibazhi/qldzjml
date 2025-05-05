import re

def read_lines(file_path):
    """读取文件内容为列表"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

def parse_line(line):
    """
    解析每一行数据，提取路径名、OCR 文字、匹配文本、匹配长度和行号。
    返回一个字典。
    """
    # 提取路径名和 OCR 文字
    path_and_text_match = re.match(r"\./selected_images/(.*?), 所有文本块中的文字: (.*?)$", line)
    if not path_and_text_match:
        return None  # 如果格式不匹配，跳过该行

    path_name = path_and_text_match.group(1)
    ocr_text = path_and_text_match.group(2)

    # 初始化匹配信息列表
    matches = []

    # 匹配全匹配或部分匹配的信息
    full_matches = re.findall(r"匹配到的标准文本: \"(.*?)\" $行号: (\d+)$", line)
    partial_matches = re.findall(r"匹配到的标准文本: \"(.*?)\" $行号: (\d+)$, 匹配部分: \"(.*?)\", 匹配长度: (\d+)", line)

    # 将全匹配加入匹配列表
    for match_text, row_number in full_matches:
        matches.append({
            "match_text": match_text,
            "match_length": "N/A",
            "match_row_number": row_number
        })

    # 将部分匹配加入匹配列表
    for match_text, row_number, partial_text, match_length in partial_matches:
        matches.append({
            "match_text": partial_text,
            "match_length": match_length,
            "match_row_number": row_number
        })

    # 如果没有匹配，则添加默认值
    if not matches:
        matches.append({
            "match_text": "未匹配",
            "match_length": "N/A",
            "match_row_number": "N/A"
        })

    # 返回解析后的数据
    return {
        "path_name": path_name,
        "ocr_text": ocr_text,
        "matches": matches
    }

def generate_html(output_file, data):
    """
    生成 HTML 文件。
    :param output_file: 输出的 HTML 文件路径
    :param data: 数据列表，每个元素是一个字典
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OCR 匹配结果</title>
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
        </style>
    </head>
    <body>
        <h1>OCR 匹配结果</h1>
        <table>
            <thead>
                <tr>
                    <th>路径名</th>
                    <th>所有 OCR 文字</th>
                    <th>匹配文本</th>
                    <th>匹配长度</th>
                    <th>行号</th>
                </tr>
            </thead>
            <tbody>
    """

    for item in data:
        ocr_text = item["ocr_text"]
        path_name = item["path_name"]
        for match in item["matches"]:
            html_content += f"""
                <tr>
                    <td>{path_name}</td>
                    <td>{ocr_text}</td>
                    <td>{match['match_text']}</td>
                    <td>{match['match_length']}</td>
                    <td>{match['match_row_number']}</td>
                </tr>
            """

    html_content += """
            </tbody>
        </table>
    </body>
    </html>
    """

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(html_content)

if __name__ == "__main__":
    input_file = "comparison_result_with_sliding_window.txt"  # 输入文件路径
    output_file = "comparison_result.html"  # 输出 HTML 文件路径

    # 读取输入文件
    lines = read_lines(input_file)

    # 解析每一行数据
    parsed_data = []
    for line in lines:
        parsed_item = parse_line(line)
        if parsed_item:
            parsed_data.append(parsed_item)

    # 生成 HTML 文件
    generate_html(output_file, parsed_data)

    print(f"HTML 文件已生成: {output_file}")
