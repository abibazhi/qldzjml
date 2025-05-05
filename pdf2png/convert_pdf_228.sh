#!/bin/bash

# 定义源PDF文件路径和输出目录
SOURCE_PDF="./P0228.pdf"  # 源PDF文件路径
OUTPUT_DIR="./output"        # 输出目录

# 创建输出目录
mkdir -p "$OUTPUT_DIR"
echo "Created or verified output directory: $OUTPUT_DIR"

# 使用 pdfinfo 获取 PDF 总页数
INFO=$(pdfinfo "$SOURCE_PDF")
if [ $? -ne 0 ]; then
    echo "Error: Failed to retrieve information from $SOURCE_PDF using pdfinfo." >&2
    exit 1
fi

# 打印pdfinfo的完整输出用于调试
echo "Debug: Output of pdfinfo:"
echo "$INFO"

# 使用 awk 提取总页数
TOTAL_PAGES=$(echo "$INFO" | awk '/^Pages:/ {print $2}')
if [ -z "$TOTAL_PAGES" ]; then
    echo "Error: Could not determine the number of pages in $SOURCE_PDF. Please check if the file exists and is a valid PDF." >&2
    exit 1
fi
echo "Processing $SOURCE_PDF with $TOTAL_PAGES pages."

# 处理每一页
for ((PAGE=0; PAGE<TOTAL_PAGES; PAGE++)); do
    IMAGE_INDEX=$(printf "%03d" $((PAGE+1)))
    OUTPUT_FILE="$OUTPUT_DIR/$IMAGE_INDEX.tiff"
    
    # 打印当前处理的页面信息
    echo "Processing page $((PAGE+1)) of $SOURCE_PDF to $OUTPUT_FILE"
    
    # 检查文件是否存在以跳过已转换的页面
    if [ ! -f "$OUTPUT_FILE" ]; then
        # 调试信息：打印将要执行的命令
        CMD="convert -density 300 \"$SOURCE_PDF[$PAGE]\" -threshold 50% -type bilevel -compress group4 \"$OUTPUT_FILE\""
        echo "Executing command: $CMD"
        
        # 执行转换命令
        convert -density 300 "$SOURCE_PDF[$PAGE]" -threshold 50% -type bilevel -compress group4 "$OUTPUT_FILE"
        
        if [ $? -ne 0 ]; then
            echo "Error converting page $((PAGE+1)) of $SOURCE_PDF." >&2
            exit 1
        fi
        
        echo "Converted page $((PAGE+1)) of $SOURCE_PDF to $OUTPUT_FILE."
    else
        echo "Skipping existing file $OUTPUT_FILE."
    fi
done

echo "All pages of $SOURCE_PDF have been successfully converted."
