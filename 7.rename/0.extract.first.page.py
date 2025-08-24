from bs4 import BeautifulSoup
import requests
import re

def extract_volume_starts():
    url = "https://daxumi.cn/"
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到所有 <tr>，提取 href 中的 start
    starts = []
    for a in soup.find_all('a', href=re.compile(r'start=\d+')):
        href = a['href']
        match = re.search(r'start=(\d{6})', href)
        if match:
            start = match.group(1)
            starts.append(start)

    # 按数字排序
    starts.sort(key=int)

    # 找出“跨册”的边界：037559 → 038008
    volume_boundaries = {}
    for i in range(1, len(starts)):
        prev, curr = starts[i-1], starts[i]
        if curr[:3] != prev[:3]:  # 册号变化
            volume = curr[:3]
            first_page = int(curr[3:])
            catalog_count = first_page - 1
            volume_boundaries[volume] = {
                'first_start': curr,
                'first_page_in_volume': first_page,
                'catalog_pages': catalog_count
            }
            print(f"第{volume}册：首经起于 {curr}，目录页数：{catalog_count}")

    return volume_boundaries

# 🔴 缺少这一行！
if __name__ == "__main__":
    result = extract_volume_starts()
    print("提取结果：", result)
