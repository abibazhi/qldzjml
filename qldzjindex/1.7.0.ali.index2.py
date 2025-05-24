from bs4 import BeautifulSoup

def parse_html_to_books(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "lxml")
    table = soup.find("table", class_="dataframe")

    books = []

    for row in table.find_all("tr")[1:]:  # 跳过表头
        cells = row.find_all("td")
        if len(cells) < 2:
            continue

        # 提取编号（原样保留）
        book_id = cells[0].get_text(strip=True)

        # 提取名称和路径
        a_tag = cells[1].find("a")
        name = a_tag.get_text(strip=True)
        path = a_tag["href"]  # 示例: qldzj/001/165

        # 构造 path 字段（如 "001/165"）
        path_parts = path.split("/")
        if len(path_parts) >= 3:
            folder = path_parts[1]  # 001
            page = path_parts[2]    # 165
            full_path = f"{folder}/{page}"
        else:
            full_path = ""  # 处理异常情况

        # 添加到 books 列表
        books.append({"name": name, "path": full_path})

    return books

# 使用示例
books = parse_html_to_books("1.5.8.ali.title和居中.html")  # 替换为你的 HTML 文件路径

# 输出结果
print("books = [")
for book in books:
    print(f'    {{"name": "{book["name"]}", "path": "{book["path"]}"}}')
print("]")
