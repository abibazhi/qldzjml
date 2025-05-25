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

echo "Deleting JPG files from 165.jpg to 662.jpg in directory $DIRECTORY..."

# 遍历并删除指定范围内的 JPG 文件
for ((i=165; i<=662; i++)); do
    FILE="$DIRECTORY/$(printf "%03d.jpg" $i)"
    if [ -f "$FILE" ]; then
        rm "$FILE"
        echo "Deleted $FILE"
    else
        echo "File $FILE does not exist. Skipping."
    fi
done

echo "All specified JPG files have been deleted."




