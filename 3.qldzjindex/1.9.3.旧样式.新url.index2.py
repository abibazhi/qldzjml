import json

# 读取JSON数据
with open('books.json', 'r', encoding='utf-8') as file:
    books = json.load(file)

# 开始构建HTML内容
html_content = """
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>乾隆大藏经目录</title>
    <style>
        body {
            font-family: "Microsoft YaHei", sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f9f9f9;
        }
        h1 {
            text-align: center;
            font-size: 2em;
            margin-bottom: 30px;
            color: #333;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 0 20px;
            background-color: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid #999;
            padding: 10px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        a {
            color: #0066cc;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>乾隆大藏经目录</h1>
    <div class="container">
        <table border="1" class="dataframe">
            <thead>
                <tr>
                    <th style="text-align: left;">编号</th>
                    <th style="text-align: left;">链接</th>
                </tr>
            </thead>
            <tbody>
"""

# 添加书籍信息到HTML
for book in books:
    html_content += f"""
                <tr>
                    <td>{book['id']}</td>
                    <td><a href="sutra.html?start={book['start'].replace('.', '')}&end={book['end'].replace('.', '')}">{book['name']}</a></td>
                </tr>
    """

# 结束HTML内容
html_content += """
            </tbody>
        </table>
    </div>
</body>
</html>
"""

# 将生成的内容写入新的HTML文件
with open('generated_sutra_catalog.html', 'w', encoding='utf-8') as result_file:
    result_file.write(html_content)
