#!/usr/bin/env bash
set -e
pdf="pdfs/001a.PDF"
out_dir="pdfs/001a"
mkdir -p "$out_dir"

# 1. 重新抽取 JPEG（保持原方向）
pdfimages -all "$pdf" "$out_dir/extract"

# 2. 找出第 2 页 1-15 条碎片并垂直拼接
mapfile -t jpg_list < <(
    pdfimages -list "$pdf" |
    awk '$2>=1 && $2<=15 {printf "%s/extract-%d.jpg\n", "'"$out_dir"'", $2}'
)

convert "${jpg_list[@]}" -append "$out_dir/page-2.jpg"

echo "完成：$out_dir/page-2.jpg"
