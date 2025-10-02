#!/bin/bash
pdf="pdfs/002.pdf"
dir="pdfs/002"

# 1. 看看 pdfimages 本身有没有 0 字节碎片
echo "=== pdfimages 原始信息 ==="
pdfimages -list "$pdf" | awk '$NF=="0K" || $NF=="0B"'

# 2. 再抽第 2 页到 tmp 目录，看实际字节
mkdir -p "$dir/tmp_re"
pdfimages -f 2 -l 2 "$pdf" "$dir/tmp_re"
ls -l "$dir/tmp_re" | awk '$5==0'

# 3. 如果 tmp_re-000.ccitt 是 0 字节，说明 PDF 里就没数据
