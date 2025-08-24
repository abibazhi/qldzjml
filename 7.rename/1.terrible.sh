cd ./qldzj/001
catalog_count=2  # 查 0.catalog.count.txt 第11行

# 手动重命名 356.png 及之后
for old in {8..164}; do
    if [ -f "$old.jpg" ]; then
        new=$((old - catalog_count))
        mv "$old.jpg" "$(printf "%03d" $new).jpg"
    fi
done
