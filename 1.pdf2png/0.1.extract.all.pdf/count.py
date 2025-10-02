#!/usr/bin/env python3
import os
import re

# 配置
BASE_DIR = "./pngs"  # 你的图片根目录

def find_dirs_with_large_pages():
    print("🔍 正在扫描 tmp/ 下的子目录...")
    print("-" * 60)

    large_dirs = []

    # 获取所有子目录：001, 002, ..., 168
    try:
        dirs = [d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d))]
        dirs.sort()  # 按目录名排序
    except FileNotFoundError:
        print(f"❌ 目录不存在: {BASE_DIR}")
        return

    for d in dirs:
        dir_path = os.path.join(BASE_DIR, d)
        png_files = [f for f in os.listdir(dir_path) if f.lower().endswith('.png')]
        
        if not png_files:
            continue

        # 提取所有页码数字
        page_numbers = []
        for f in png_files:
            # 匹配任意位数的数字：1.png, 001.png, 1000.png
            match = re.match(r'^(\d+)\.png$', f, re.IGNORECASE)
            if match:
                page_numbers.append(int(match.group(1)))

        if not page_numbers:
            continue

        max_page = max(page_numbers)
        total_files = len(png_files)

        if max_page > 999:
            large_dirs.append(d)
            print(f"🚨 {d}/ 最大页码: {max_page:4d} | 共 {total_files:3d} 个 PNG 文件")
        else:
            print(f"✅ {d}/ 最大页码: {max_page:4d} | 共 {total_files:3d} 个 PNG 文件")

    print("-" * 60)
    
    if large_dirs:
        print(f"🔴 发现 {len(large_dirs)} 个目录最大页码 > 999：")
        for d in large_dirs:
            print(f"     → {d}/")
    else:
        print("🟢 所有目录页码均 ≤ 999，无需特殊处理")

if __name__ == "__main__":
    find_dirs_with_large_pages()
