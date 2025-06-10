import json

# 读取JSON数据
with open('stura.translator.0.add.translator.to.json.py.json', 'r', encoding='utf-8') as file:
    books = json.load(file)

# 过滤掉 id 为 null、"NaN" 或空字符串的条目
filtered_books = []
for book in books:
    book_id = book.get("id")
    if book_id is None:
        continue
    if isinstance(book_id, str) and book_id.strip().lower() == "nan":
        continue
    if book_id == "":
        continue
    filtered_books.append(book)

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
            max-width: 1000px;
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
                    <th style="text-align: left;">经文名称</th>
                    <th style="text-align: left;">译者</th>
                </tr>
            </thead>
            <tbody>
"""

# 添加书籍信息到HTML
for book in filtered_books:
    name = book.get("name", "")
    book_id = book.get("id", "")
    translator = book.get("translator", "")

    # 处理译者字段：如果是 null 或 NaN，显示为空字符串
    if translator is None or (isinstance(translator, float) and str(translator) == "nan"):
        translator = ""

    # 构造链接中的 start 和 end 参数（去掉小数点）
    start = book['start'].replace('.', '')
    end = book['end'].replace('.', '')

    html_content += f"""
                <tr>
                    <td>{book_id}</td>
                    <td><a href="sutra.html?start={start}&end={end}">{name}</a></td>
                    <td>{translator}</td>
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
with open('generated_sutra_catalog_with_translator_3_columns.html', 'w', encoding='utf-8') as result_file:
    result_file.write(html_content)

print("✅ 已完成 HTML 文件生成（三列：编号、链接、译者）")
