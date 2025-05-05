from bs4 import BeautifulSoup
import re


# 读取本地HTML文件的内容
with open('qldzj-ml.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 第一步：删除包含“部 号”的<tr>...</tr>行块
rows = soup.find_all('tr')
for row in rows:
    if any('部 号' in td.get_text() for td in row.find_all('td')):
        row.decompose()

# 第二步：删除包含“第*册”的<td>...</td>块
all_tds = soup.find_all('td')
for td in all_tds:
    if re.search(r'第\d+册', td.get_text()):
        td.decompose()

# 第三步：处理rowspan
rows = soup.find_all('tr')
rowspan_mapping = {}
new_rows = []

for i, row in enumerate(rows):
    cols = row.find_all('td')
    new_cols = []
    for j, col in enumerate(cols):
        rowspan = int(col.get('rowspan', 1))
        if rowspan > 1:
            rowspan_mapping[(i, j)] = {'rowspan': rowspan, 'value': col.get_text(strip=True)}
        if (i, j) in rowspan_mapping:
            new_cols.append(soup.new_tag('td'))
            new_cols[-1].string = rowspan_mapping[(i, j)]['value']
            for k in range(1, rowspan_mapping[(i, j)]['rowspan']):
                next_row = rows[i + k]
                next_col = next_row.find_all('td')[j]
                next_col.decompose()
            del rowspan_mapping[(i, j)]
        else:
            new_cols.append(col)
    new_row = soup.new_tag('tr')
    for new_col in new_cols:
        new_row.append(new_col)
    new_rows.append(new_row)

# 重新构建表格
new_table = soup.new_tag('table')
for new_row in new_rows:
    new_table.append(new_row)
soup.find('table').replace_with(new_table)

# 将修改后的HTML写回到文件中
with open('qldzj-ml_modified.html', 'w', encoding='utf-8') as file:
    file.write(str(soup))

print("处理完成，已生成qldzj-ml_modified.html")

