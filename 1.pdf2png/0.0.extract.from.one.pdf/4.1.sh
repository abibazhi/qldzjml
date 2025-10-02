#!/usr/bin/env bash
# 把当前目录下所有 extract-*.ccitt 按页转 PNG
# 临时文件放在 /tmp，最后删除

# 1. 先拿 pdfimages 列表
pdfimages -list 038.pdf > /tmp/img.lst

while IFS= read -r line; do
    [[ $line =~ ^page ]] && continue
    set -- $line
    page=$1 ; num=$2 ; w=$4 ; h=$5 ; dpi_x=$9 ; dpi_y=$10

    # 2. 构造输出文件名
    out="page-$(printf %03d $page).png"

    # 3. 把裸 CCITT 包成 TIFF（加 Group4 头）
    tif="/tmp/extract-$num.tiff"
# 注意：-size 必须放在最前；+repage 防止警告
    convert  -size ${w}x${h} -density ${dpi_x}x${dpi_y} -compress Group4 +repage \
             "extract-$num.ccitt"  "$tif"

    # 4. TIFF → PNG
    convert "$tif" "$out"

    # 5. 清理
    rm -f "$tif"
done < /tmp/img.lst
