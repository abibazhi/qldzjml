#!/usr/bin/env bash
shopt -s globstar           # 确保 globstar 打开
base=$(date -d "today 00:00" +%s)

# 收集待优化文件
mapfile -t todo < <(ls -1 pdfs/**/*.png 2>/dev/null | sort)
total=${#todo[@]}
[[ $total -eq 0 ]] && { echo "无任务"; exit 0; }

printf "待优化：%d 个\n" "$total"
printf "%s\n" "${todo[@]}" | xargs -P$(nproc) -I{} \
    sh -c 'optipng -o7 -strip all "{}" && echo "✓ {}"'
