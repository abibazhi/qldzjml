#!/usr/bin/env python3
import os
import re

# 配置
BASE_DIR = "./pngs"
CATALOG_COUNT_FILE = "./0.catalog.count.txt"

def natural_sort_key(filename):
    """自然排序 key：提取文件名中的数字"""
    match = re.search(r'^(\d+)', filename)
    return int(match.group(1)) if match else 0

def main():
    print("🔧 开始处理目录页重命名...")
    
    # 读取目录页数
    try:
        with open(CATALOG_COUNT_FILE, 'r', encoding='utf-8') as f:
            catalog_counts = [int(line.strip()) for line in f if line.strip().isdigit()]
    except Exception as e:
        print(f"❌ 读取 {CATALOG_COUNT_FILE} 失败: {e}")
        return

    if len(catalog_counts) != 168:
        print(f"⚠️  注意：catalog.count.txt 有 {len(catalog_counts)} 行，预期 168 行")

    # 处理每个目录
    for idx, catalog_count in enumerate(catalog_counts, start=1):
        vol_dir = os.path.join(BASE_DIR, f"{idx:03d}")
        
        if not os.path.exists(vol_dir):
            print(f"❌ 目录不存在: {vol_dir}")
            continue

        print(f"\n📁 处理册子 {idx:03d} (目录页数: {catalog_count})")

        # 获取所有 .png 文件并按自然数排序
        png_files = [f for f in os.listdir(vol_dir) if f.lower().endswith('.png')]
        png_files.sort(key=natural_sort_key)

        if len(png_files) < catalog_count:
            print(f"❌ 警告: 文件数({len(png_files)}) < 目录页数({catalog_count})")
            continue

        # === 阶段 1：重命名目录页 ===
        for i in range(catalog_count):
            old_name = png_files[i]
            new_name = f"C{i+1}.png"
            old_path = os.path.join(vol_dir, old_name)
            new_path = os.path.join(vol_dir, new_name)

            if os.path.exists(new_path):
                print(f"❌ 冲突: {new_path} 已存在，跳过")
                continue

            os.rename(old_path, new_path)
            print(f"   📂 目录页: {old_name} → {new_name}")

        # === 阶段 2：重命名正文页 ===
        body_start = catalog_count
        for i, old_name in enumerate(png_files[body_start:], start=1):
            new_name = f"{i}.png"
            old_path = os.path.join(vol_dir, old_name)
            new_path = os.path.join(vol_dir, new_name)

            if old_path == new_path:
                continue  # 已经是正确名字

            if os.path.exists(new_path):
                print(f"❌ 冲突: {new_path} 已存在，跳过 {old_name}")
                continue

            os.rename(old_path, new_path)
            print(f"   📘 正文页: {old_name} → {new_name}")

    print("\n✅ 所有册子处理完成！")

if __name__ == "__main__":
    main()
