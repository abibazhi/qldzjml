import requests
from bs4 import BeautifulSoup

# 下载网页内容并保存为本地文件
url = 'http://www.qldzj.com/html/qldzj-ml.htm'
response = requests.get(url)
response.encoding = 'utf-8'  # 设置响应的编码为UTF-8

# 将网页内容保存到本地文件
with open('qldzj-ml.html', 'w', encoding='utf-8') as file:
    file.write(response.text)

# 读取本地文件的内容
with open('qldzj-ml.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 查找所有<tr>...</tr>行
rows = soup.find_all('tr')

for row in rows:
    # 获取所有的<td>标签
    cols = row.find_all('td')
    
    # 如果该行包含至少两个<td>标签，则移除第二个<td>
    if len(cols) > 1:
        second_td = cols[1]
        # 清空第二个<td>标签的内容
        second_td.string = ''
        # 如果需要完全移除第二个<td>标签而不是清空其内容，请使用下面的代码：
        # second_td.decompose()

# 将修改后的HTML写回到文件中
with open('qldzj-ml_modified.html', 'w', encoding='utf-8') as file:
    file.write(str(soup))

print("处理完成，已生成qldzj-ml_modified.html")
