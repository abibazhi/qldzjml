import os
import re

# 配置
BASE_DIR = "./tmp"           # qldzj 目录路径
CATALOG_FILE = "0.catalog.count.txt"  # 目录页数文件

def read_catalog_counts():
    """读取 0.catalog.count.txt，返回列表"""
    counts = []
    with open(CATALOG_FILE, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if line.isdigit():
                counts.append(int(line))
            else:
                print(f"⚠️ 第 {line_num} 行不是数字: '{line}'，跳过")
    print(f"✅ 成功读取 {len(counts)} 册目录页数")
    return counts
def rename_images():
    # 读取每册的目录页数
    catalog_counts = read_catalog_counts()

    # 遍历每一册
    for volume_idx in range(1, len(catalog_counts) + 1):
        volume = f"{volume_idx:03d}"  # 001, 002, ..., 168
        vol_dir = os.path.join(BASE_DIR, volume)

        if not os.path.exists(vol_dir):
            print(f"❌ 目录不存在: {vol_dir}")
            continue

        catalog_count = catalog_counts[volume_idx - 1]  # 列表从0开始
        print(f"\n--- 处理第 {volume} 册 (目录页数: {catalog_count}) ---")

        # 获取该目录下所有 .png 文件
        files = [f for f in os.listdir(vol_dir) if f.lower().endswith('.png')]
        files.sort()  # 确保顺序

        # === 阶段 0：统一文件名为三位数格式 ===
        print("🔄 阶段 0: 统一文件名格式为三位数")
        temp_renamed = []  # 记录临时重命名，避免冲突

        for file_name in files:
            # 跳过已处理的 C001.png 或非 .png
            if file_name.startswith('C') or not file_name.lower().endswith('.png'):
                continue

            # 匹配 1.png, 2.png, ..., 999.png
            match = re.match(r'^(\d+)\.png$', file_name, re.IGNORECASE)
            if not match:
                continue

            num = int(match.group(1))
            new_name = f"{num:03d}.png"

            if file_name == new_name:
                continue  # 已经是三位数，跳过

            old_path = os.path.join(vol_dir, file_name)
            new_path = os.path.join(vol_dir, new_name)

            # 检查目标是否已存在
            if os.path.exists(new_path):
                print(f"❌ 冲突: {new_path} 已存在，跳过 {file_name}")
                continue

            os.rename(old_path, new_path)
            temp_renamed.append((file_name, new_name))
            print(f"   {file_name} → {new_name}")

        # 更新文件列表（重新获取）
        files = [f for f in os.listdir(vol_dir) if f.lower().endswith('.png')]
        files.sort()

        # === 阶段 1：重命名目录页 001.png → C001.png ===
        print("📁 阶段 1: 重命名目录页")
        for i in range(1, catalog_count + 1):
            old_name = f"{i:03d}.png"
            new_name = f"C{i:03d}.png"
            old_path = os.path.join(vol_dir, old_name)
            new_path = os.path.join(vol_dir, new_name)

            if os.path.exists(old_path):
                if os.path.exists(new_path):
                    print(f"❌ 冲突: {new_path} 已存在，跳过 {old_name}")
                else:
                    os.rename(old_path, new_path)
                    print(f"   {old_name} → {new_name}")
            # else: 缺失页，跳过

        # === 阶段 2：重命名正文页 008.png → 001.png ===
        print("📄 阶段 2: 重命名正文页")
        for file_name in files:
            if file_name.startswith('C') or not file_name.endswith('.png'):
                continue

            match = re.match(r'^(\d{3})\.png$', file_name)
            if not match:
                continue

            page_num = int(match.group(1))
            if page_num <= catalog_count:
                continue  # 已处理为 C00x.png

            new_page = page_num - catalog_count
            new_name = f"{new_page:03d}.png"
            old_path = os.path.join(vol_dir, file_name)
            new_path = os.path.join(vol_dir, new_name)

            if os.path.exists(new_path):
                print(f"❌ 冲突: {new_path} 已存在，跳过 {file_name}")
            else:
                os.rename(old_path, new_path)
                print(f"   {file_name} → {new_name}")

        print(f"✅ 第 {volume} 册重命名完成")

    print("\n🎉 所有册处理完成！")

def rename_images1():
    # 读取每册的目录页数
    catalog_counts = read_catalog_counts()
    
    # 遍历每一册
    for volume_idx in range(1, len(catalog_counts) + 1):
        volume = f"{volume_idx:03d}"  # 001, 002, ..., 168
        vol_dir = os.path.join(BASE_DIR, volume)
        
        if not os.path.exists(vol_dir):
            print(f"❌ 目录不存在: {vol_dir}")
            continue
            
        catalog_count = catalog_counts[volume_idx - 1]  # 列表从0开始
        print(f"\n--- 处理第 {volume} 册 (目录页数: {catalog_count}) ---")
        
        # 获取该目录下所有 .png 文件
        files = [f for f in os.listdir(vol_dir) if f.lower().endswith('.png')]
        files.sort()  # 确保顺序
        
        # 两阶段重命名：先改目录页，再改正文页
        renamed = []

        # === 第一阶段：重命名目录页 001.png → C001.png ===
        for i in range(1, catalog_count + 1):
            old_name = f"{i:03d}.png"
            new_name = f"C{i:03d}.png"
            old_path = os.path.join(vol_dir, old_name)
            new_path = os.path.join(vol_dir, new_name)
            
            if os.path.exists(old_path):
                if os.path.exists(new_path):
                    print(f"❌ 冲突: {new_path} 已存在，跳过 {old_name}")
                else:
                    os.rename(old_path, new_path)
                    renamed.append((old_name, new_name))
                    print(f"📁 目录页: {old_name} → {new_name}")
            # else: 可能缺失，跳过

        # === 第二阶段：重命名正文页 008.png → 001.png ===
        for file_name in files:
            # 跳过已处理的目录页和已改名的 C001.png
            if file_name.startswith('C') or not file_name.endswith('.png'):
                continue
                
            # 匹配 008.png, 123.png 等
            match = re.match(r'^(\d{3})\.png$', file_name)
            if not match:
                continue
                
            page_num = int(match.group(1))
            
            # 只处理大于 catalog_count 的页
            if page_num <= catalog_count:
                continue  # 已处理为 C00x.png
                
            new_page = page_num - catalog_count
            new_name = f"{new_page:03d}.png"
            old_path = os.path.join(vol_dir, file_name)
            new_path = os.path.join(vol_dir, new_name)
            
            if os.path.exists(new_path):
                print(f"❌ 冲突: {new_path} 已存在，跳过 {file_name}")
            else:
                os.rename(old_path, new_path)
                renamed.append((file_name, new_name))
                print(f"📄 正文页: {file_name} → {new_name}")
        
        print(f"✅ 第 {volume} 册重命名完成")

    print("\n🎉 所有册处理完成！")

# =============== 运行脚本 ===============
if __name__ == "__main__":
    print("🔄 开始批量重命名图片文件...")
    rename_images()
