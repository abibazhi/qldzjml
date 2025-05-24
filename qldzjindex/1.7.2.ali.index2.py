import json

# 读取 JSON 文件
def load_books_from_json(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

# 生成 HTML 内容
def generate_html(books):
    html_content = """
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>乾隆大藏经目录</title>
    <style>
        body { font-family: "Microsoft YaHei", sans-serif; margin: 0; padding: 20px; background-color: #f9f9f9; }
        h1 { text-align: center; font-size: 2em; margin-bottom: 30px; color: #333; }
        .container { max-width: 800px; margin: 0 auto; padding: 0 20px; background-color: white; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #999; padding: 10px; text-align: left; }
        th { background-color: #f2f2f2; }
        a { color: #0066cc; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>乾隆大藏经目录</h1>
    <div class="container">
        <table border="1" class="dataframe">
            <thead><tr><th style="text-align: left;">编号</th><th style="text-align: left;">链接</th></tr></thead>
            <tbody>
"""

    for i, book in enumerate(books):
        path_parts = book["path"].split("/")
        if len(path_parts) < 3:
            continue
        prefix = path_parts[1]  # 前三位
        suffix = path_parts[2]  # 后三位
        start = f"{prefix}{suffix}"  # start = 001165

        # 计算 end
        if i + 1 < len(books):
            next_book = books[i + 1]
            next_path_parts = next_book["path"].split("/")
            next_prefix = next_path_parts[1]
            next_suffix = str(int(next_path_parts[2]) - 1).zfill(3)
            end = f"{next_prefix}{next_suffix}"
        else:
            # 最后一部经的 end 固定为 168748
            end = "168748"

        # 构造链接
        link = f'<a href="yourpage.html?start={start}&end={end}">{book["name"]}</a>'
        html_content += f'                <tr><td>{book["no"]}</td><td>{link}</td></tr>\n'

    html_content += """
            </tbody>
        </table>
    </div>
</body>
</html>
"""
    return html_content

# 主程序
if __name__ == "__main__":
    json_file = "books.json"  # 替换为你的 JSON 文件路径
    output_html = "qldzj_index.html"

    books = load_books_from_json(json_file)
    html_content = generate_html(books)

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ HTML 目录已生成：{output_html}")
