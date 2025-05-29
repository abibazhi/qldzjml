import json

def generate_index_html(json_file, output_file):
    """
    从 JSON 文件生成 index.html 目录页面
    - 每个书目链接格式为: sutra.html?start=001165&end=014084
    - start: 六位数格式，前三位为册号，后三位为页号
    - end: 同上，若 end 为 '000.000' 表示该书没有结束页
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            books = json.load(f)
    except FileNotFoundError:
        print(f"❌ 输入文件 {json_file} 不存在！")
        return

    html_content = """
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>乾隆大藏经目录</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            padding: 20px;
        }
        h1 {
            color: #333;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            margin-bottom: 10px;
        }
        a {
            text-decoration: none;
            color: #007BFF;
            font-weight: bold;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
<h1>乾隆大藏经目录</h1>
<ul>
"""

    for book in books:
        # 提取 start 和 end 字段
        start = book.get("start", "001.001")  # 默认值
        end = book.get("end", "000.000")

        # 转换为六位数格式
        start_clean = start.replace('.', '')
        end_clean = end.replace('.', '') if end != "000.000" else ""

        # 构建链接（关键改动在这里）
        link = f"sutra.html?start={start_clean}"
        if end_clean:
            link += f"&end={end_clean}"

        # 构建 HTML 列表项
        html_content += f'<li><a href="{link}">{book.get("name", "未知书籍")}</a></li>\n'

    html_content += """
</ul>
</body>
</html>
"""

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ 已成功生成目录文件：{output_file}")
    except Exception as e:
        print(f"❌ 写入输出文件失败：{e}")

# 示例调用
if __name__ == "__main__":
    json_input = 'books_with_pages.json'  # 替换为你的 JSON 文件名
    output_html = 'index.html'
    generate_index_html(json_input, output_html)
