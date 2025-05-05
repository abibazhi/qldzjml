#!/bin/bash

# 定义基础目录和输出目录
base_dir="/mnt/d/qldzjtiff"  # 根据实际情况设置基础目录
input_dir="$base_dir/output"  # 输入目录，即之前的输出目录
output_dir="$base_dir/png_output"  # 新的输出目录用于存放PNG文件

# 创建输出目录
mkdir -p "$output_dir"
echo "Created or verified output directory: $output_dir"

# 检查输入目录是否存在
if [ ! -d "$input_dir" ]; then
    echo "Error: Input directory does not exist: $input_dir" >&2
    exit 1
fi

echo "Processing TIFF files in directory: $input_dir"

# 遍历所有tiff文件并进行转换
for file in "$input_dir"/*.tiff; do
    # 如果没有匹配的文件，则跳过
    if [ ! -e "$file" ]; then
        echo "No TIFF files found in $input_dir"
        break
    fi

    # 获取文件名（不包含扩展名）
    base=$(basename "$file" .tiff)

    # 确定输出文件路径
    output_file="$output_dir/${base}.png"

    # 执行转换
    if convert "$file" "$output_file"; then
        echo "Converted $file to $output_file"
        # 可选：删除原始tiff文件
        rm "$file" && echo "Deleted original TIFF file: $file"
    else
        echo "Failed to convert $file"
    fi
done

echo "All TIFF files have been successfully converted to PNG."
