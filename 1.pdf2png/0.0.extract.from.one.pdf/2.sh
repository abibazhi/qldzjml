#!/usr/bin/env bash
# 依赖：sudo apt install imagemagick

shopt -s nullglob            # 防止没匹配到时把字面量 * 传进去
for ccitt in *.ccitt; do
    base=${ccitt%.ccitt}     # 去掉扩展名，如 038-000

    # 读 .params 第一行
    read params < "${base}.params"

    # 用 eval 把这一行当作 convert 的参数
    # 例如：convert -4 -p -x 1120 -B -M 038-000.ccitt 038-000.png
    eval convert $params "${ccitt}" "${base}.png"
done

# 如果想合成一份 PDF：
# convert *.png all_pages.pdf
