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

# 第三步：处理含有 rowspan 属性的列
rows = soup.find_all('tr')
i = 0
while i < len(rows):
    row = rows[i]
    cols = row.find_all('td')
    for col in cols:
        rowspan = col.get('rowspan')
        if rowspan:
            rowspan = int(rowspan)
            # 移除 rowspan 属性
            del col['rowspan']
            # 删除接下来指定行数的行
            for _ in range(rowspan - 1):
                if i + 1 < len(rows):
                    next_row = rows[i + 1]
                    next_row.decompose()
                    rows = soup.find_all('tr')  # 重新获取行列表，因为结构已改变
    i += 1

# 将修改后的HTML写回到文件中
with open('qldzj-ml_modified.html', 'w', encoding='utf-8') as file:
    file.write(str(soup))

print("处理完成，已生成qldzj-ml_modified.html")
