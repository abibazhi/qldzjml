#!/bin/bash

# 设置源目录和目标临时目录
src_dir="$PWD/qldzjpng"
temp_dir="/tmp/qldzj_temp"

print(src_dir)
print(temp_dir)

# 导出LC_ALL以避免可能遇到的本地化问题
export LC_ALL=C

# 使用find命令查找大于80KB(即81920字节)的文件
find "$src_dir" -type f -size +80k | while read -r file; do
    # 计算相对路径并构造目标路径
    relative_path="${file#$src_dir/}"
    dest_file="$temp_dir/$relative_path"
    
    # 创建必要的目录结构
    mkdir -p "$(dirname "$dest_file")"
    
    # 拷贝文件
    cp "$file" "$dest_file"
    
    echo "Copied $file to $dest_file"
done
