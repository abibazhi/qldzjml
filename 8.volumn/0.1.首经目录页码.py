from bs4 import BeautifulSoup
import re

def update_sutra_href(html_path, last_volume_max_pages):
    """
    批量修改目录HTML的href链接格式
    :param html_path: 原HTML文件路径（如"目录.html"）
    :param last_volume_max_pages: 字典，存储每册最后一卷的最大页码（如{14: 69}表示14册最后一页是69）
    """
    # 1. 读取原HTML文件并备份
    with open(html_path, 'r', encoding='utf-8') as f:
        original_html = f.read()
    
    # 自动备份原文件（避免误操作丢失数据）
    backup_path = html_path.replace('.html', '_backup.html')
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(original_html)
    print(f"✅ 已备份原文件至：{backup_path}")

    # 2. 解析HTML，提取所有目录链接
    soup = BeautifulSoup(original_html, 'html.parser')
    # 定位所有目录链接（匹配原href="/qldzj/xx/xx"格式）
    link_pattern = re.compile(r'^/qldzj/(\d+)/(\d+)$')
    links = []
    for a_tag in soup.find_all('a', href=link_pattern):
        match = link_pattern.match(a_tag['href'])
        volume = int(match.group(1))  # 册号（如14）
        page = int(match.group(2))    # 当前卷起始页码（如1）
        links.append({
            'tag': a_tag,
            'volume': volume,
            'start_page': page
        })
    print(f"✅ 共识别到 {len(links)} 个目录链接")

    # 3. 批量计算并修改href
    for i in range(len(links)):
        current = links[i]
        volume = current['volume']
        start_page = current['start_page']
        
        # 计算start：册号3位补零 + 页码3位补零（如14册1页→014001）
        start = f"{volume:03d}{start_page:03d}"
        
        # 计算end：优先取下一卷的start_page-1，若无下一卷则用配置的“册最大页码”
        if i < len(links) - 1:
            next_link = links[i+1]
            # 若下一卷属于同一册，则end = 下一卷start_page - 1
            if next_link['volume'] == volume:
                end_page = next_link['start_page'] - 1
            # 若下一卷属于不同册，则end = 当前册的最大页码（从配置中取）
            else:
                end_page = last_volume_max_pages.get(volume, start_page)  # 兜底用当前页
        # 最后一个链接（全文件最后一卷），直接用配置的最大页码
        else:
            end_page = last_volume_max_pages.get(volume, start_page)
        
        # 计算end：册号3位补零 + 结束页码3位补零（如14册17页→014017）
        end = f"{volume:03d}{end_page:03d}"
        
        # 修改href属性
        new_href = f"sutra.html?start={start}&end={end}"
        current['tag']['href'] = new_href
        print(f"📄 第{volume}册 第{start_page}页 → href: {new_href}")

    # 4. 保存修改后的HTML文件
    modified_html = soup.prettify()
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(modified_html)
    print(f"\n✅ 所有链接修改完成！已保存至原文件：{html_path}")


# -------------------------- 配置参数（请根据你的实际情况修改）--------------------------
if __name__ == "__main__":
    # 1. 你的目录HTML文件路径（如放在桌面则写"C:/Users/用户名/Desktop/目录.html"）
    HTML_FILE_PATH = "1.html"  # 替换为你的文件路径
    
    # 2. 配置每册最后一卷的“最大页码”（关键！需与你的目录实际页码对应）
    # 格式：{册号: 该册最后一页页码, ...}（1-14册按你提供的目录整理）
    LAST_VOLUME_MAX_PAGES = {
        1: 660,    # 假设第1册最后一页是747（需替换为你第1册实际最大页码）
        2: 820,    # 替换为第2册实际最大页码
        3: 766,    # 替换为第3册实际最大页码
        4: 756,    # 替换为第4册实际最大页码
        5: 766,    # 替换为第5册实际最大页码
        6: 768,    # 替换为第6册实际最大页码
        7: 706,    # 替换为第7册实际最大页码
        8: 718,    # 替换为第8册实际最大页码
        9: 730,    # 第9册最后一页
        10: 716,   # 第10册最后一页
        11: 742,   # 第11册最后一页
        12: 764,   # 第12册最后一页
        13: 732,   # 第13册最后一页
        14: 82     # 第14册最后一页
    }
    
    # 执行修改（运行后会自动备份+修改）
    update_sutra_href(HTML_FILE_PATH, LAST_VOLUME_MAX_PAGES)
