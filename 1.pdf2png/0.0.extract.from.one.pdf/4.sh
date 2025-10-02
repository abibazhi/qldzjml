#!/usr/bin/env bash
# 依赖：sudo apt install imagemagick ghostscript bc

# 1. 先拿到 pdfimages 的完整列表，存成临时文件
pdfimages -list 038.pdf > /tmp/img.lst

# 2. 读取列表并处理
idx=0                  # 当前物理页号（1 开始）
start=-1               # 当前页第一条序号
while IFS= read -r line; do
    [[ $line =~ ^page ]] && continue      # 跳过表头
    # 用 awk 切出各字段
    set -- $line
    page=$1 ; num=$2 ; width=$4 ; height=$5 ; xppi=$9 ; yppi=$10

    # 遇到新页 → 处理上一页
    if [[ $page -ne $idx ]]; then
        if [[ $start -ge 0 ]]; then
            # 计算序号范围
            last=$((num - 1))
            if [[ $start -eq $last ]]; then
                # 单幅图
                infile=$(printf "extract-%03d.ccitt" $start)
                convert  -size ${width}x${height} -density ${xppi}x${yppi} \
                         -compress Group4 "$infile" "page-$(printf %03d $idx).png"
            else
                # 多条幅 → 纵向拼接
                montage extract-$(printf %03d $start)-$(printf %03d $last).ccitt \
                        -tile 1x -geometry ${width}x${height}+0+0 \
                        -density ${xppi}x${yppi} -compress Group4 \
                        "page-$(printf %03d $idx).png"
            fi
        fi
        idx=$page
        start=$num
    fi
done < /tmp/img.lst

# 处理最后一页
last=$(pdfimages -list 038.pdf | tail -1 | awk '{print $2}')
if [[ $start -eq $last ]]; then
    convert -size ${width}x${height} -density ${xppi}x${yppi} \
            -compress Group4 "$(printf extract-%03d.ccitt $start)" \
            "page-$(printf %03d $idx).png"
else
    montage extract-$(printf %03d $start)-$(printf %03d $last).ccitt \
            -tile 1x -geometry ${width}x${height}+0+0 \
            -density ${xppi}x${yppi} -compress Group4 \
            "page-$(printf %03d $idx).png"
fi
