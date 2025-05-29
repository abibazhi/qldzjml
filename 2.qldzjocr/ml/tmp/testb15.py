import requests
from bs4 import BeautifulSoup

# 获取网页内容
url = 'http://www.qldzj.com/html/qldzj-ml.htm'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# 找到所有表格
tables = soup.find_all('table')

for table in tables:
    rows = table.find_all('tr')
    # 用于记录当前 rowspan 剩余的行数
    rowspan_counts = []
    for row in rows:
        cols = row.find_all('td')
        new_cols = []
        index = 0
        for col in cols:
            rowspan = int(col.get('rowspan', 1))
            if index == 1:
                # 如果是第二列，跳过
                if rowspan > 1:
                    # 记录 rowspan 剩余行数
                    rowspan_counts.append(rowspan - 1)
                index += 1
                continue
            if rowspan_counts and rowspan_counts[0] > 0:
                # 如果前面有未结束的 rowspan，跳过该列
                rowspan_counts[0] -= 1
                if rowspan_counts[0] == 0:
                    rowspan_counts.pop(0)
                index += 1
                continue
            new_cols.append(col)
            index += 1
            if rowspan > 1:
                # 记录新的 rowspan 剩余行数
                rowspan_counts.append(rowspan - 1)

        # 清空当前行的内容
        row.clear()
        # 添加新的列到当前行
        for new_col in new_cols:
            row.append(new_col)

# 保存修改后的网页内容为新的 HTML 文件
with open('modified.html', 'w', encoding='utf-8') as file:
    file.write(soup.prettify())
