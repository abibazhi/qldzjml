import requests
from bs4 import BeautifulSoup

# 获取网页内容
url = 'http://www.qldzj.com/html/qldzj-ml.htm'
response = requests.get(url)
html_content = response.text

# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 找到所有表格行
rows = soup.find_all('tr')

# 初始化变量以保存提取的数据
extracted_data = []

# 遍历每一行，并提取第一列和第三列的内容
for row in rows:
    cols = row.find_all('td')
    if len(cols) >= 3:  # 确保该行有至少三列
        buhao = cols[0].get_text(strip=True)
        jingming = cols[2].get_text(strip=True)
        
        # 如果第一列为空，则认为它是前一行的延续
        if not buhao.strip():
            if extracted_data:
                # 更新上一个条目的经名
                if isinstance(extracted_data[-1]['经名'], list):
                    extracted_data[-1]['经名'].append(jingming)
                else:
                    extracted_data[-1]['经名'] = [extracted_data[-1]['经名'], jingming]
        else:
            # 如果当前行的第一列不为空，则添加新条目
            extracted_data.append({
                '部名': buhao,
                '经名': jingming
            })

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
                <th>部名</th>
                <th>经名</th>
            </tr>
        </thead>
        <tbody>
'''

# 添加提取的数据到HTML表格
for item in extracted_data:
    jingming = item['经名'][0] if isinstance(item['经名'], list) else item['经名']
    output_html += f'<tr><td>{item["部名"]}</td><td>{jingming}</td></tr>\n'

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
