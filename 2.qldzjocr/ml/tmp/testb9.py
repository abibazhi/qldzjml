import requests
from bs4 import BeautifulSoup

# 指定网页URL
url = 'http://www.qldzj.com/html/qldzj-ml.htm'

# 发送HTTP请求获取网页内容
response = requests.get(url)
if response.status_code != 200:
    raise Exception(f"Failed to fetch the page. Status code: {response.status_code}")

# 解析HTML内容
soup = BeautifulSoup(response.content, 'html.parser')

# 查找表格
table = soup.find('table')

# 初始化结果列表
results = []

# 遍历表格的每一行
for row in table.find_all('tr'):
    cols = row.find_all('td')
    if len(cols) > 2:
        # 提取第一列和第三列的内容
        bu_name = cols.get_text(strip=True)
        jing_name = cols‌:ml-citation{ref="1" data="citationList"}.get_text(strip=True)
        # 将提取的信息添加到结果列表中
        results.append((bu_name, jing_name))

# 初始化输出HTML文档内容
output_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>乾隆大藏经目录提取</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #000;
            padding: 8px;
            text-align: left;
        }
    </style>
</head>
<body>
    <table>
        <thead>
            <tr>
                <th>部名</th>
                <th>经名</th>
            </tr>
        </thead>
        <tbody>
"""

# 将结果添加到输出HTML文档中
for bu_name, jing_name in results:
    output_html += f"            <tr>\n                <td>{bu_name}</td>\n                <td>{jing_name}</td>\n            </tr>\n"

# 完成输出HTML文档内容
output_html += """
        </tbody>
    </table>
</body>
</html>
"""

# 将输出HTML文档内容保存到文件
with open('extracted_qldzj_ml.html', 'w', encoding='utf-8') as file:
    file.write(output_html)

print("HTML文档已保存为extracted_qldzj_ml.html")
