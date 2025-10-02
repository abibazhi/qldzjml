#!/bin/bash

META_FILE="image_metadata.txt"

# 生成元数据（如果不存在）
if [[ ! -f "$META_FILE" ]]; then
  echo "📊 正在提取图像元数据..."
  pdfimages -list 038.pdf | awk 'NF>=7 && $3=="image" {print $4, $5}' > "$META_FILE"
fi

# 获取所有 .ccitt 文件
mapfile -t ccitt_files < <(ls 038-*.ccitt | sort)

# 逐个处理
for i in "${!ccitt_files[@]}"; do
  ccitt_file="${ccitt_files[i]}"
  base=$(basename "$ccitt_file" .ccitt)
  param_file="${base}.params"
  webp_file="${base}.webp"

  # ✅ 提取宽度
  width=$(awk '{for(i=1;i<=NF;i++) if($i=="-X") print $(i+1); exit}' "$param_file")
  if [[ -z "$width" || ! "$width" =~ ^[0-9]+$ ]]; then
    echo "❌ 无法提取有效宽度: $param_file"
    continue
  fi

  # ✅ 提取高度（第二列）
  height=$(sed -n "$((i+1))p" "$META_FILE" | awk '{print $2}')
  if [[ -z "$height" || ! "$height" =~ ^[0-9]+$ ]]; then
    echo "❌ 无法提取有效高度: 行 $((i+1))"
    continue
  fi

  echo "📄 处理 $ccitt_file (宽度: ${width}, 高度: ${height})"

  # ✅ 使用 gray: 模式读取原始位图
  convert \
    -depth 1 \
    -colorspace Gray \
    -monochrome \
    -endian MSB \
    -size ${width}x${height} \
    gray:"$ccitt_file" \
    -compress Group4 \
    -define tiff:fill-order=msb \
    "/tmp/${base}.tiff"

  if [[ $? -ne 0 ]]; then
    echo "❌ TIFF 转换失败: $ccitt_file"
    continue
  fi

  # ✅ 转为 WebP
  convert "/tmp/${base}.tiff" -define webp:lossless=true "$webp_file"
  rm -f "/tmp/${base}.tiff"

  echo "✅ 成功: $webp_file"
done
