def parse_file_content(file_content):
    lines = file_content.splitlines()
    results = []
    for line in lines:
        # 提取文件名
        file_name = line.split(',')[0].split('/')[-1]

        # 提取所有文本块中的文字
        all_text_start = line.find('所有文本块中的文字:') + len('所有文本块中的文字:')
        all_text_end = line.find('|', all_text_start)
        if all_text_end == -1:
            all_text_end = line.find('(全匹配:', all_text_start)
            if all_text_end == -1:
                all_text_end = line.find('(部分匹配:', all_text_start)
        all_text = line[all_text_start:all_text_end].strip()

        # 提取匹配类型、匹配文字和行号
        if '| 未匹配' in line:
            match_type = '不匹配'
            match_text = '无'
            line_number = '无'
        elif '(全匹配:' in line:
            match_type = '全匹配'
            match_text = re.search(r'\(全匹配: "(.*?)"', line).group(1)
            line_number = re.search(r'\(行号: (\d+)\)', line).group(1)
        elif '(部分匹配:' in line:
            match_type = '部分匹配'
            match_text = re.search(r'\(部分匹配: "(.*?)"', line).group(1)
            line_number = re.search(r'\(行号: (\d+)\)', line).group(1)
        else:
            match_type = '不匹配'
            match_text = '无'
            line_number = '无'

        results.append({
            '文件名': file_name,
            '所有文本块中的文字': all_text,
            '匹配类型': match_type,
            '匹配文字': match_text,
            '行号': line_number
        })
    return results

def convert_to_html(parsed_results, output_file):
    html_content = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>OCR匹配结果</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px auto;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #f8f9fa;
            font-weight: bold;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .match-type {
            text-align: center;
        }
        .match-text {
            max-width: 400px;
            white-space: normal;
        }
    </style>
</head>
<body>
    <h1>OCR匹配结果分析</h1>
    <table>
        <thead>
            <tr>
                <th>文件名</th>
                <th>所有文本块中的文字</th>
                <th>匹配类型</th>
                <th>匹配文字</th>
                <th>行号</th>
            </tr>
        </thead>
        <tbody>
    """

    for result in parsed_results:
        html_content += f"""
            <tr>
                <td>{result['文件名']}</td>
                <td class="match-text">{result['所有文本块中的文字']}</td>
                <td class="match-type">{result['匹配类型']}</td>
                <td class="match-text">{result['匹配文字']}</td>
                <td>{result['行号']}</td>
            </tr>
        """

    html_content += """
        </tbody>
    </table>
</body>
</html>
    """

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

# 使用示例
file_content = """
./selected_images/qldzjpng_164_003.png, 所有文本块中的文字: 成唯識音響補遣, 成雅識音響補遣, 清武林蓮居绍覺大師音, 法嗣智素補, 新伊大師合, 菊比, 美我 成唯识音响补遣 成雅识音响补遣 清武林莲居绍觉大师音 法嗣智素补 新伊大师合 美我 | 未匹配
./selected_images/qldzjpng_165_003.png, 所有文本块中的文字: 妙法蓮華經授手, 妙法蓮華經授手, 清楚衡雲案沙門智祥集 妙法莲华经授手 妙法莲华经授手 清楚衡云案沙门智祥集 (部分匹配: "妙 法莲华经授手（第01卷～第20卷）" (行号: 1663), 匹配部分: "妙法莲华经授手", 匹配长度: 7)
./selected_images/qldzjpng_166_003.png, 所有文本块中的文字: 賢首五教儀, 賢首五教儀, 清浙水慈云沙門灌頂法集录 贤首五教仪 贤首五教仪 清浙水慈云沙门灌顶法集录 (全匹配: "贤首五教仪" (行号: 1664))
./selected_images/qldzjpng_166_177.png, 所有文本块中的文字: 重訂教乘法數, 重訂教秉法數 重订教乘法数 重订教秉法数 (全匹配: "重订教乘法数" (行号: 1665))
./selected_images/qldzjpng_167_003.png, 所有文本块中的文字: 御選語錄, 御選語錄 御选语录 御选语录 | 未匹配
./selected_images/qldzjpng_168_003.png, 所有文本块中的文字: 御錄宗镜大網, 御錄宗鏡大, 慧日·水明妙圆正修智覺禮師二 御录宗镜大网 御录宗镜大 慧日·水明妙圆正修智觉礼师二 (部分匹配: " 御录宗镜大纲" (行号: 1667), 匹配部分: "御录宗镜大", 匹配长度: 5)
./selected_images/qldzjpng_168_331.png, 所有文本块中的文字: 御錄经海一滴, 御绿經海一滴 御录经海一滴 御绿经海一滴 (全匹配: "御录经海一滴" (行号: 1668))
"""

parsed_results = parse_file_content(file_content)
convert_to_html(parsed_results, 'ocr_matching_report.html')
