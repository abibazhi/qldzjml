from bs4 import BeautifulSoup

# 读取本地HTML文件的内容
with open('qldzj-ml.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 查找所有<tr>...</tr>行块
rows = soup.find_all('tr')

# 遍历每一个<tr>...</tr>行块
for row in rows:
    # 检查<tr>标签内的文本是否包含"部 号"
    if any('部 号' in td.get_text() for td in row.find_all('td')):
        # 删除整个<tr>...</tr>块
        row.decompose()

# 将修改后的HTML写回到文件中
with open('qldzj-ml_modified.html', 'w', encoding='utf-8') as file:
    file.write(str(soup))

print("处理完成，已生成qldzj-ml_modified.html")
