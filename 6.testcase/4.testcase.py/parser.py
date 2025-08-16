# parser.py
from bs4 import BeautifulSoup
import requests
import os
from typing import Dict
from sutra import Sutra

URL = "http://daxumi.cn/index.html"
LOCAL_FILE = "index.html"

def download_index():
    print("正在下载 index.html...")
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        with open(LOCAL_FILE, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("下载完成。")
    except Exception as e:
        print(f"下载失败: {e}，将尝试使用本地文件。")

def parse_index(force_download=False) -> Dict[int, Sutra]:
    """
    解析 index.html，返回 {编号: Sutra} 的字典
    """
    if force_download or not os.path.exists(LOCAL_FILE):
        download_index()

    try:
        with open(LOCAL_FILE, 'r', encoding='utf-8') as f:
            html = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"未找到 {LOCAL_FILE}，请确保已下载。")

    soup = BeautifulSoup(html, 'html.parser')
    suttas: Dict[int, Sutra] = {}
    current_section = ""

    for row in soup.select('table.dataframe tr'):
        section_header = row.select_one('td[colspan="2"] strong')
        if section_header:
            current_section = section_header.get_text(strip=True)
            continue

        cells = row.find_all('td')
        if len(cells) != 3:
            continue

        try:
            number = int(cells[0].get_text(strip=True))
            title_link = cells[1].find('a')
            title = title_link.get_text(strip=True) if title_link else ""

            href = title_link.get('href') if title_link else ""
            start_page = end_page = ""
            if 'start=' in href and 'end=' in href:
                import re
                start_match = re.search(r'start=(\d+)', href)
                end_match = re.search(r'end=(\d+)', href)
                start_page = start_match.group(1) if start_match else ""
                end_page = end_match.group(1) if end_match else ""

            author = cells[2].get_text(strip=True)

            suttas[number] = Sutra(
                number=number,
                title=title,
                author=author,
                start_page=start_page,
                end_page=end_page,
                section=current_section
            )
        except (ValueError, AttributeError) as e:
            print(f"解析第 {len(suttas)+1} 行失败: {e}")
            continue

    print(f"共解析 {len(suttas)} 条佛典数据。")
    return suttas
