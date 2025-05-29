import requests

# 下载网页内容并保存为本地文件
url = 'http://www.qldzj.com/html/qldzj-ml.htm'
response = requests.get(url)
response.encoding = 'utf-8'  # 设置响应的编码为UTF-8

# 将网页内容保存到本地文件
with open('1.qldzj-ml.html', 'w', encoding='utf-8') as file:
    file.write(response.text)


print("处理完成，已下载qldzj-ml.html")
