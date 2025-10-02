#!/usr/bin/env bash

# 定义要处理的目录
base_dir="pdfs"
dirs=("001a" "001b" "001c" "001d" "001e")

# 遍历指定的目录
for dir in "${dirs[@]}"; do
    full_dir="$base_dir/$dir"
    if [ -d "$full_dir" ]; then
        echo "正在处理目录: $full_dir"
        # 遍历目录中的所有以 tmp 开头的 JPG 文件
        for file in "$full_dir"/tmp*.jpg; do
            if [ -f "$file" ]; then
                echo "上下反转图片: $file"
                # 使用 ImageMagick 将图片上下反转
                convert "$file" -flip "$file"
            fi
        done
    else
        echo "目录不存在: $full_dir"
    fi
done

echo "指定目录中的所有以 tmp 开头的 PNG 图片已上下反转"
