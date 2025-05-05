import requests
from bs4 import BeautifulSoup

# 目标网页的URL
url = 'http://www.qldzj.com/html/qldzj-ml.htm'

# 获取网页内容
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# 用于存储提取信息的列表
data = []

# 遍历所有表格
tables = soup.find_all('table')
for table in tables:
    rows = table.find_all('tr')
    for i, row in enumerate(rows):
        cols = row.find_all('td')
        if len(cols) >= 3:
            # 提取第一列和第三列的文本内容
            part_name = cols[0].get_text(strip=True)
            # 如果第一列的一行对应第三列的多行，则取该第三列中相对应的第二行作为经名
            if len(rows) > i + 1:
                next_row_cols = rows[i + 1].find_all('td')
                if len(next_row_cols) >= 3:
                    scripture_name = next_row_cols[2].get_text(strip=True)
                else:
                    scripture_name = cols[2].get_text(strip=True)
            else:
                scripture_name = cols[2].get_text(strip=True)
            data.append((part_name, scripture_name))

# 输出提取的信息
for part, scripture in data:
    print(f"部名: {part}, 经名: {scripture}")
