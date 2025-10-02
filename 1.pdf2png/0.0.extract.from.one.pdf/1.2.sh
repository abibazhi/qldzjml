#!/bin/bash

# 创建临时文件存储元数据
META_FILE="image_metadata.txt"

# 如果元数据文件不存在，则生成它
if [[ ! -f "$META_FILE" ]]; then
  echo "📊 正在提取图像元数据..."
  pdfimages -list 038.pdf | awk 'NF>=7 && $3=="image" {print $1, $4, $5}' > "$META_FILE"
fi

# 提取所有 .ccitt 文件，按顺序处理
mapfile -t ccitt_files < <(ls 038-*.ccitt | sort)

# 初始化计数器
metadata_index=0

for ccitt_file in "${ccitt_files[@]}"; do
  base=$(basename "$ccitt_file" .ccitt)
  param_file="${base}.params"
  webp_file="${base}.webp"

  # 从 .params 文件中读取宽度
  width=$(awk '/-X/ {print $2; exit}' "$param_file")
  if [[ -z "$width" ]]; then
    echo "❌ 无法提取宽度: $param_file"
    continue
  fi

  # 从元数据文件中读取高度
  read page_num height <<< $(sed -n "$((metadata_index+1))p" "$META_FILE")

  # 验证宽高
  if [[ -z "$height" ]]; then
    echo "❌ 无法读取高度: 行 $((metadata_index+1))"
    metadata_index=$((metadata_index + 1))
    continue
  fi

  echo "📄 处理 $ccitt_file (宽度: ${width}, 高度: ${height})"

  # 转换为 TIFF
  convert \
    -depth 1 \
    -colorspace Gray \
    -monochrome \
    -define tiff:fill-order=msb \
    -compress Group4 \
    -size ${width}x${height} \
    "ccitt:$ccitt_file" \
    "/tmp/${base}.tiff"

  if [[ $? -ne 0 ]]; then
    echo "❌ 转换失败: $ccitt_file"
    metadata_index=$((metadata_index + 1))
    continue
  fi

  # TIFF → WebP
  convert "/tmp/${base}.tiff" -define webp:lossless=true "$webp_file"
  rm -f "/tmp/${base}.tiff"

  if [[ $? -eq 0 ]]; then
    echo "✅ 成功: $webp_file"
  else
    echo "❌ 失败: $ccitt_file"
  fi

  # 更新元数据索引
  metadata_index=$((metadata_index + 1))
done
