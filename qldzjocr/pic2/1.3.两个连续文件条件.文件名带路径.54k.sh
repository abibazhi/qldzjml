#!/bin/bash

# 设置源目录和目标临时目录
src_dir="/home/jm/dev/qldzjocr/pic2/qldzjpng/"
temp_dir="/tmp/qldzj_temp"

# 确保目标临时目录存在
mkdir -p "$temp_dir"

# 使用-L跟随符号链接并查找所有文件，按路径排序
find -L "$src_dir" -type f | sort | while read -r file; do
    # 获取当前文件大小
    size=$(stat -c%s "$file")
    
    # 检查文件大小是否在54k到65k之间
    if [ $size -ge 54272 ] && [ $size -le 66560 ]; then
        # 获取下一个文件（假设是紧接着的下一个）
        next_file=$(find -L "$src_dir" -type f | sort | grep -A1 "$file" | tail -n1)
        
        # 如果next_file为空或者不是文件，则跳过
        if [[ ! -f "$next_file" ]]; then
            continue
        fi
        
        # 获取下一个文件的大小
        next_size=$(stat -c%s "$next_file")

        # 检查下一个文件是否存在且大于80k
        if [ $next_size -gt 87040 ]; then
            # 构造新的文件名，保留原始路径以防重复
            new_name1="${temp_dir}/$(basename "$src_dir")_$(echo "$file" | sed "s|${src_dir}||" | tr '/' '_')"
            new_name2="${temp_dir}/$(basename "$src_dir")_$(echo "$next_file" | sed "s|${src_dir}||" | tr '/' '_')"

            # 拷贝文件到临时目录，使用新文件名
            cp "$file" "$new_name1"
            cp "$next_file" "$new_name2"
            
            echo "Copied $file to $new_name1 and $next_file to $new_name2"
        fi
    fi
done
