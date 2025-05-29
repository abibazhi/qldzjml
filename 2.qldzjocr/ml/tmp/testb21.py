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

# 第三步：处理 rowspan，合并相应的行
table = soup.find('table')
if table:
    rows = table.find_all('tr')
    i = 0
    while i < len(rows):
        row = rows[i]
        cols = row.find_all('td')
        for j, col in enumerate(cols):
            rowspan = col.get('rowspan')
            if rowspan:
                rowspan = int(rowspan)
                # 移除多余的行
                for k in range(1, rowspan):
                    next_row = rows[i + k]
                    next_cols = next_row.find_all('td')
                    if j < len(next_cols):
                        next_cols[j].decompose()
                    # 如果该行没有任何列了，移除该行
                    if not next_row.find_all('td'):
                        next_row.decompose()
                # 移除当前单元格的 rowspan 属性
                del col['rowspan']
        i += 1

# 将修改后的HTML写回到文件中
with open('qldzj-ml_modified.html', 'w', encoding='utf-8') as file:
    file.write(str(soup))

print("处理完成，已生成qldzj-ml_modified.html")
