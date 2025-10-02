#!/usr/bin/env bash
# 设置基准时间
base=$(date -d "today 17:45" +%s)

# 目录列表（001a,001b…168）
#dirs=(pngs/001{a..e} pngs/{002..168})
dirs=(pdfs/*/)

total_dirs=${#dirs[@]}
for ((i=0;i<total_dirs;i++)); do
    dir=${dirs[$i]}
    [[ ! -d $dir ]] && continue

    # 该目录待优化文件
    mapfile -t todo < <(find "$dir" -name '*.png' ! -newermt "@$base")
    cnt=${#todo[@]}
    [[ $cnt -eq 0 ]] && { printf "[%02d/%02d] %s 已完成\n" $((i+1)) $total_dirs "$dir"; continue; }

    printf "[%02d/%02d] %s 开始 (%d 个)\n" $((i+1)) $total_dirs "$dir" "$cnt"
    printf '%s\n' "${todo[@]}" | xargs -P$(nproc) -I{} optipng -o7 -strip all "{}"
done

echo "全部目录处理完成"
