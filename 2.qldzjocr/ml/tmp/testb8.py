import requests
from bs4 import BeautifulSoup

# 获取网页内容
url = 'http://www.qldzj.com/html/qldzj-ml.htm'
response = requests.get(url)
response.encoding = 'utf-8'  # 设置响应的编码为UTF-8
html_content = response.text

# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 找到所有表格行
rows = soup.find_all('tr')

# 初始化变量以保存提取的数据
extracted_data = []
current_buhao = None

# 遍历每一行，并提取第一列和第三列的内容
for row in rows:
    cols = row.find_all('td')
    if len(cols) >= 3:  # 确保该行有至少三列
        buhao = cols[0].get_text(strip=True)
        jingming = cols[2].get_text(strip=True)

        # 如果当前行的第一列不为空，则这是一个新的部号
        if buhao.strip():
            current_buhao = buhao
            extracted_data.append({
                '部号': current_buhao,
                '经名': jingming
            })
        else:
            # 当前行的第一列为空，表示它是前一行的延续
            if current_buhao and extracted_data:
                # 如果之前的部号已经有经名，我们不需要重复添加
                continue

# 将提取的数据写入新的HTML文件
output_html = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>提取的乾隆大藏经目录</title>
</head>
<body>
    <table border="1">
        <thead>
            <tr>
                <th>部号</th>
                <th>经名</th>
            </tr>
        </thead>
        <tbody>
'''

# 添加提取的数据到HTML表格
for item in extracted_data:
    output_html += f'<tr><td>{item["部号"]}</td><td>{item["经名"]}</td></tr>\n'

output_html += '''
        </tbody>
    </table>
</body>
</html>
'''

# 写入文件
with open('extracted_qldzj.html', 'w', encoding='utf-8') as file:
    file.write(output_html)

print("提取完成，已生成extracted_qldzj.html")
