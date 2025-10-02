#!/usr/bin/env bash

# ========== 配置 ==========
src_dirs=(pngs/001{a..e})    # 源目录：001a, 001b, ..., 001e
dst_dir="pngs/001"           # 目标目录
# ==========================

# 检查源目录
for dir in "${src_dirs[@]}"; do
    if [[ ! -d "$dir" ]]; then
        echo "❌ 源目录不存在: $dir"
        exit 1
    fi
done

# 创建目标目录
mkdir -p "$dst_dir"

echo "🚀 开始合并 ${src_dirs[*]} 到 $dst_dir"

counter=1

for dir in "${src_dirs[@]}"; do
    echo "📂 处理 $dir"
    
    # 获取该目录下所有 .png 文件，按文件名排序
    while IFS= read -r -d '' file; do
        # 格式化序号为 3 位：001, 002, ...
        new_name=$(printf "%03d.png" $counter)
        cp "$file" "$dst_dir/$new_name"
        echo "   $file → $new_name"
        ((counter++))
    done < <(find "$dir" -name "*.png" -type f -print0 | sort -z)
done

echo "✅ 合并完成！共 $((counter-1)) 个文件，已保存到 $dst_dir"
