import os
import re
from pathlib import Path

# 主目录路径
base_dir = Path("/mnt/d/qldzj/pngs")

# 用于存储结果的字典
max_files = {}

# 遍历 001 到 168 的子目录
for i in range(1, 169):
    subdir_name = f"{i:03d}"  # 格式化为 001, 002, ..., 168
    subdir_path = base_dir / subdir_name

    if not subdir_path.exists() or not subdir_path.is_dir():
        print(f"目录不存在或不是目录: {subdir_path}")
        continue

    # 获取所有 .png 文件，提取纯数字文件名
    png_files = []
    for file in subdir_path.iterdir():
        if file.is_file() and file.suffix.lower() == ".png":
            # 使用正则匹配纯数字文件名，如 1.png, 2.png 等
            match = re.fullmatch(r"(\d+)\.png", file.name)
            if match:
                png_files.append(int(match.group(1)))

    if png_files:
        max_num = max(png_files)
        max_files[subdir_name] = max_num
        print(f"子目录 {subdir_name}: 最大编号文件是 {max_num}.png")
    else:
        print(f"子目录 {subdir_name}: 未找到符合命名规则的 .png 文件")
        max_files[subdir_name] = None

# 如果你想把结果保存到文件中，比如 JSON
import json
with open("max_png_numbers.json", "w", encoding="utf-8") as f:
    json.dump(max_files, f, ensure_ascii=False, indent=4)

print("所有子目录处理完成，结果已保存到 max_png_numbers.json")
