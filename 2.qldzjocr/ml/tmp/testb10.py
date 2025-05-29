import requests
from bs4 import BeautifulSoup

# 获取网页内容
url = 'http://www.qldzj.com/html/qldzj-ml.htm'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# 找到所有表格
tables = soup.find_all('table')

for table in tables:
    # 遍历表格中的每一行
    for row in table.find_all('tr'):
        cols = row.find_all('td')
        # 如果该行有至少3列，删除第二列
        if len(cols) >= 3:
            cols[1].decompose()

# 保存修改后的网页内容为新的HTML文件
with open('modified.html', 'w', encoding='utf-8') as file:
    file.write(soup.prettify())
