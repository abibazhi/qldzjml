#!/bin/bash

# 检查是否提供了目录路径
if [ -z "$1" ]; then
    echo "Usage: $0 <directory_path>"
    exit 1
fi

DIRECTORY="$1"

# 检查目录是否存在
if [ ! -d "$DIRECTORY" ]; then
    echo "Directory $DIRECTORY does not exist."
    exit 1
fi

echo "Deleting TIFF files from 1.tiff to 164.tiff in directory $DIRECTORY..."

# 遍历并删除指定范围内的 TIFF 文件
for ((i=1; i<=164; i++)); do
    FILE="$DIRECTORY/$(printf "%03d.tiff" $i)"
    if [ -f "$FILE" ]; then
        rm "$FILE"
        echo "Deleted $FILE"
    else
        echo "File $FILE does not exist. Skipping."
    fi
done

echo "All specified TIFF files have been deleted."




