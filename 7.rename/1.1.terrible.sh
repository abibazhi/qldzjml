cd ./qldzj/001
catalog_count=2

# 定义起始和结束页（原始文件名中的数字）
start_page=3
end_page=164

for file in *.jpg; do
    [[ -f "$file" ]] || continue
    [[ "$file" == C* ]] && continue

    if [[ "$file" =~ ^([0-9]+)\.jpg$ ]]; then
        page_str="${BASH_REMATCH[1]}"
        page_num=$((10#$page_str))

        # 只处理目录之后的正文页（且在指定范围内）
        if (( page_num > catalog_count && page_num >= start_page && page_num <= end_page )); then
            new_page=$((page_num - catalog_count))
            new_name=$(printf "%03d.jpg" $new_page)
            
            if [[ ! -f "$new_name" ]]; then
                mv "$file" "$new_name"
                echo "🔄 $file → $new_name"
            else
                echo "❌ 已存在: $new_name，跳过 $file"
            fi
        fi
    fi
done
