from bs4 import BeautifulSoup
import re

# 读取本地HTML文件的内容
with open('qldzj-ml.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 第一步：删除包含“部 号”的<tr>...</tr>行块
rows = soup.find_all('tr')
rows_to_delete = []
for row in rows:
    if any('部 号' in td.get_text() for td in row.find_all('td')):
        rows_to_delete.append(row)

for row in rows_to_delete:
    row.decompose()

# 第二步：删除包含“第*册”的<td>...</td>块
all_tds = soup.find_all('td')
for td in all_tds:
    if re.search(r'第\d+册', td.get_text()):
        td.decompose()

# 第三步：处理带有rowspan属性的<td>标签
rows = soup.find_all('tr')
rows_to_skip = set()
for i, row in enumerate(rows):
    cols = row.find_all('td')
    for j, col in enumerate(cols):
        if col.has_attr('rowspan'):
            rowspan_value = int(col['rowspan'])
            # 删除当前行之后的rowspan_value - 1行
            for k in range(1, rowspan_value):
                if (i + k) < len(rows):
                    rows_to_skip.add(i + k)

# 删除需要跳过的行
for index in sorted(rows_to_skip, reverse=True):
    rows[index].decompose()

# 将修改后的HTML写回到文件中
with open('qldzj-ml_modified.html', 'w', encoding='utf-8') as file:
    file.write(str(soup))

print("处理完成，已生成qldzj-ml_modified.html")
