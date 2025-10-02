#!/usr/bin/env bash
shopt -s nullglob
for ccitt in *.ccitt; do
    base=${ccitt%.ccitt}
    read params < "${base}.params"        # 读整行
    gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m \
       -r204x196 -g"${params#*-x }"x      # 用 .params 里的宽度动态生成
       -sOutputFile="${base}.png" \
       -f "$ccitt"
done
