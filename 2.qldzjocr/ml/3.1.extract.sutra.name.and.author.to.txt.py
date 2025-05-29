from bs4 import BeautifulSoup
import re

# 读取本地HTML文件的内容
with open('1.qldzj-ml.html', 'r', encoding='utf-8') as file:
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
            del col['rowspan']
            for _ in range(rowspan - 1):
                if i + 1 < len(rows):
                    next_row = rows[i + 1]
                    next_row.decompose()
                    rows = soup.find_all('tr')
    # 处理“目录”结尾情况
    if len(cols) > 1:
        second_col = cols[1]
        a_tag = second_col.find('a')
        if a_tag:
            text = a_tag.get_text(strip=True)
            if text.endswith('目录'):
                new_text = text[:-2]
                a_tag.string = new_text
    i += 1

# 第四步：处理连续的空白行，只保留一个
rows = soup.find_all('tr')
prev_blank = False
i = 0
while i < len(rows):
    row = rows[i]
    if not row.get_text(strip=True):
        if prev_blank:
            row.decompose()
            rows = soup.find_all('tr')
        else:
            prev_blank = True
            i += 1
    else:
        prev_blank = False
        i += 1

# 提取经名和作者到文本文件
sutra_author_pairs = []

# 遍历所有行
rows = soup.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    if len(cols) < 4:
        continue  # 忽略列数不足的行
    
    # 提取第二列（经名）
    sutra_col = cols[1]
    a_tag = sutra_col.find('a')
    if a_tag:
        sutra_name = a_tag.get_text(strip=True)
    else:
        sutra_name = sutra_col.get_text(strip=True)
    
    # 提取第四列（作者）
    author_col = cols[3]
    author = author_col.get_text(strip=True)
    
    # 组合为"经名,作者"格式
    pair = f"{sutra_name},{author}"
    sutra_author_pairs.append(pair)

# 写入文件
with open('3.sutra-name-and-author.txt', 'w', encoding='utf-8') as txt_file:
    for line in sutra_author_pairs:
        txt_file.write(line + '\n')

print("经名和作者已提取并保存到 sutra-name-and-author.txt")
