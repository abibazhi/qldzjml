#!/bin/bash

# 设置源目录和目标临时目录
src_dir="/home/jm/dev/qldzjocr/pic2/qldzjpng/"
temp_dir="/tmp/qldzj_temp"
export LC_ALL=C

# 创建临时目录
mkdir -p "$temp_dir"

# 使用-L跟随符号链接并查找所有文件
find -L "$src_dir" -type f | sort | while read -r file; do
    # 获取文件大小
    size=$(stat -c%s "$file")
    
    # 如果文件大小在55k到65k之间
    if [ $size -ge 55000 ] && [ $size -le 65000 ]; then
        # 读取下一个文件
        next_file=$(readlink -f "$(find -L "$src_dir" -type f | grep -A1 "$file" | tail -n1)")
        next_size=$(stat -c%s "$next_file")

        # 检查下一个文件是否存在且大于80k
        if [ -f "$next_file" ] && [ $next_size -gt 81920 ]; then
            # 计算相对路径并构造目标路径
            relative_path="${file#$src_dir}"
            dest_dir="$temp_dir/$(dirname "$relative_path")"
            
            # 创建必要的目录结构
            mkdir -p "$dest_dir"
            
            # 拷贝文件
            cp --parents "$file" "$temp_dir"
            cp --parents "$next_file" "$temp_dir"
            
            echo "Copied $file and $next_file to $temp_dir"
        fi
    fi
done
