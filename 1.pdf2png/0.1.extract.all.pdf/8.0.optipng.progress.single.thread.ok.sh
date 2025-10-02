#!/usr/bin/env bash
# 基准时间：今天 00:00
base=$(date -d "today 00:00" +%s)

# 需要优化的文件列表（按子目录排序）
mapfile -t todo < <(find pdfs/** -name '*.png' ! -newermt "@$base" | sort)

total=${#todo[@]}
[[ $total -eq 0 ]] && { echo "所有 PNG 已优化"; exit 0; }

echo "待优化：$total 个"

for ((i=0;i<total;i++)); do
    f=${todo[$i]}
    printf "\r进度 %3d/%d  %s" $((i+1)) $total "$f"
    optipng -o7 -strip all "$f"
done
echo -e "\n全部完成"
