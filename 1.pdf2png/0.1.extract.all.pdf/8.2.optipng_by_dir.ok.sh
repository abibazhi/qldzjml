#!/usr/bin/env bash

# ✅ 固定基准时间：2025年9月1日 00:00:00
base=$(date -d "2025-09-07 17:45:00" +%s)

DONE_FILE=".optipng_done"
dirs=(pngs/001{a..e} pngs/{002..168})

total_dirs=${#dirs[@]}
processed=0

for ((i=0; i<total_dirs; i++)); do
    dir=${dirs[$i]}
    [[ ! -d "$dir" ]] && continue

    cd "$dir" || continue

    # 只处理：文件是 PNG + 修改时间早于 9月1日 00:00 + 不在 .optipng_done 中
    mapfile -t todo < <(
        find . -name '*.png' -type f \
            ! -newermt "@$base" \
            ! -exec grep -qF {} "$DONE_FILE" \; -print 2>/dev/null \
        | sort
    )
    cnt=${#todo[@]}

    if [[ $cnt -eq 0 ]]; then
        printf "[%02d/%02d] %s 已完成\n" "$((i+1))" "$total_dirs" "$dir"
        cd - >/dev/null || exit
        continue
    fi

    printf "[%02d/%02d] %s 开始 (%d 个)\n" "$((i+1))" "$total_dirs" "$dir" "$cnt"


    printf '%s\n' "${todo[@]}" | xargs -P$(nproc) -I{} sh -c "
    optipng -o7 -strip all '{}' > /dev/null 2>&1 &&
    echo '✅ {}' &&
    echo '{}' >> '$DONE_FILE'
"
    #printf '%s\n' "${todo[@]}" | xargs -P$(nproc) -I{} sh -c \
        #'optipng -o7 -strip all "{}" > /dev/null 2>&1 && echo "✅ {}" && echo "{}" >> "'"$DONE_FILE"'"

    cd - >/dev/null || exit
done

echo "全部目录处理完成"
