from bs4 import BeautifulSoup
import re

# 示例：替换为你的HTML文件路径
html_file = 'sutra1.vols.html'

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
mismatches = []

for tr in soup.find_all('tr'):
    for td in tr.find_all('td'):
        a = td.find('a')
        if not a:
            continue
        href = a.get('href')
        match = re.search(r'start=(\d{6})', href)
        if not match:
            continue
        # 提取 start 参数的后三位（即实际页码）
        start_page = int(match.group(1)[-3:])  # 取后三位

        # 获取显示的页码
        page_span = td.find('span', class_='page')
        if not page_span:
            continue
        try:
            display_page = int(page_span.get_text(strip=True))
        except ValueError:
            print(f"⚠️ 页码解析失败：{page_span.get_text(strip=True)}")
            continue

        # 获取标题
        title_span = td.find('span', class_='title')
        title = title_span.get_text(strip=True) if title_span else "未知"

        # 比较后三位页码
        if start_page != display_page:
            mismatches.append({
                'title': title,
                'href_start': match.group(1),
                'parsed_start_page': start_page,
                'display_page': display_page
            })

# 输出结果
if mismatches:
    print("❌ 发现页码不一致的条目：")
    print("-" * 60)
    for m in mismatches:
        print(f"标题: {m['title']}")
        print(f"  href start = {m['href_start']} → 解析页码: {m['parsed_start_page']}")
        print(f"  显示页码     = {m['display_page']}")
        print()
else:
    print("✅ 所有条目的页码（后三位）均一致！")
