import re
from pathlib import Path

# 配置
INDEX_FILE = "index.html"
CATALOG_FILE = "0.catalog.count.txt"
OUTPUT_FILE = "index_new.html"  # 输出新文件，确认无误后可重命名

def read_catalog_counts():
    """读取每册目录页数，返回列表，索引=册号-1"""
    with open(CATALOG_FILE, 'r', encoding='utf-8') as f:
        return [int(line.strip()) for line in f if line.strip().isdigit()]

def parse_volume_page(page_id):
    """解析 001165 → (1, 165)"""
    vol = int(page_id[:3])
    page = int(page_id[3:])
    return vol, page

def build_new_id(vol, page):
    """构建新ID: (1, 163) → 001163"""
    return f"{vol:03d}{page:03d}"

def update_index_html():
    counts = read_catalog_counts()
    print(f"✅ 加载 {len(counts)} 册目录页数")

    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    def replace_match(match):
        param = match.group(1)  # start 或 end
        old_id = match.group(2)
        
        try:
            vol, page = parse_volume_page(old_id)
            if vol < 1 or vol > len(counts):
                print(f"⚠️  册号超出范围: {vol} (总 {len(counts)} 册)")
                return match.group(0)
                
            catalog_count = counts[vol - 1]
            new_page = page - catalog_count
            if new_page < 1:
                print(f"⚠️  新页号小于1: {vol}-{page} - {catalog_count} = {new_page}")
                return match.group(0)
                
            new_id = build_new_id(vol, new_page)
            print(f"🔗 {param}={old_id} → {new_id}")
            return f'{param}={new_id}'
            
        except Exception as e:
            print(f"❌ 解析失败: {old_id}, {e}")
            return match.group(0)

    # 正则匹配 start=001165 和 end=014084
    pattern = r'(start|end)=(\d{6})'
    new_content = re.sub(pattern, replace_match, content)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"\n✅ 已生成新文件: {OUTPUT_FILE}")
    print("请检查无误后，手动替换原 index.html")

# =============== 运行 ===============
if __name__ == "__main__":
    update_index_html()
