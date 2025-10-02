#!/usr/bin/env python3
import os
import re

# 配置
BASE_DIR = "./pngs"  # 你的图片根目录

def restore_to_natural_numbers():
    print("🔧 正在将补零文件名恢复为自然数格式...")
    print(f"📁 扫描目录: {BASE_DIR}")
    print("-" * 60)

    processed = 0
    errors = 0

    # 遍历 tmp 下的所有子目录
    for vol_name in os.listdir(BASE_DIR):
        vol_dir = os.path.join(BASE_DIR, vol_name)
        
        if not os.path.isdir(vol_dir):
            continue

        print(f"\n📂 处理册子: {vol_name}")

        # 收集所有 .png 文件
        files = [f for f in os.listdir(vol_dir) if f.lower().endswith('.png')]
        
        if not files:
            continue

        # 按数字大小排序，从大到小处理，避免重名冲突
        def extract_num(f):
            match = re.match(r'^0*(\d+)\.png$', f, re.IGNORECASE)
            return int(match.group(1)) if match else 0
        
        # 排序：数字大的在前（先处理 099.png，再处理 9.png）
        files.sort(key=extract_num, reverse=True)

        for file_name in files:
            match = re.match(r'^0+(\d+)\.png$', file_name, re.IGNORECASE)
            if not match:
                # 不是以 0 开头，或只有一位数如 1.png，跳过
                continue

            original_num = match.group(1)  # 如 '001' → '1', '099' → '99'
            new_name = f"{original_num}.png"  # → '1.png', '99.png'
            old_path = os.path.join(vol_dir, file_name)
            new_path = os.path.join(vol_dir, new_name)

            # 检查目标文件是否已存在
            if os.path.exists(new_path):
                print(f"❌ 跳过: {file_name} → {new_name} (目标已存在)")
                errors += 1
                continue

            # 重命名
            try:
                os.rename(old_path, new_path)
                print(f"   {file_name} → {new_name}")
                processed += 1
            except Exception as e:
                print(f"💥 重命名失败: {file_name} → {new_name} | {e}")
                errors += 1

    print("-" * 60)
    print(f"✅ 完成！共处理 {processed} 个文件")
    if errors:
        print(f"⚠️  警告: {errors} 个问题（如文件冲突）")
    else:
        print(f"🎉 所有补零文件已恢复为自然数命名！")

if __name__ == "__main__":
    restore_to_natural_numbers()
