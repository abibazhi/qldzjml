def convert_to_html(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    html_content = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>转换结果</title>
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
    <table>
        <tr>
            <th>路径名</th>
            <th>所有ocr文字</th>
            <th>匹配文本</th>
            <th>匹配长度</th>
            <th>行号</th>
        </tr>
    """

    for line in lines:
        parts = line.split(',', 1)
        path = parts[0].replace('./selected_images/', '')
        text_part = parts[1].strip()

        all_ocr_text = text_part.split('(匹配到的标准文本:')[0].strip()
        match_texts = []
        match_lengths = []
        line_numbers = []

        match_parts = text_part.split('(匹配到的标准文本:')
        for match_part in match_parts[1:]:
            match_text = match_part.split('(行号:')[0].strip()
            line_number = match_part.split('(行号:')[1].split(')')[0].strip()
            match_length = 0
            if '匹配长度:' in match_part:
                match_length = match_part.split('匹配长度:')[1].split(')')[0].strip()
            match_texts.append(match_text)
            match_lengths.append(match_length)
            line_numbers.append(line_number)

        if not match_texts:
            match_texts = ['无']
            match_lengths = ['无']
            line_numbers = ['无']

        html_content += f"""
        <tr>
            <td>{path}</td>
            <td>{all_ocr_text}</td>
            <td>{', '.join(match_texts)}</td>
            <td>{', '.join(match_lengths)}</td>
            <td>{', '.join(line_numbers)}</td>
        </tr>
        """

    html_content += """
    </table>
</body>
</html>
    """

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)


input_file = 'comparison_result_with_sliding_window.txt'
output_file = 'result.html'
convert_to_html(input_file, output_file)
