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

  # ✅ 正确提取宽度：找到 -X 后面的数字
  width=$(awk '{for(i=1;i<=NF;i++) if($i=="-X") print $(i+1); exit}' "$param_file")
  if [[ -z "$width" || ! "$width" =~ ^[0-9]+$ ]]; then
    echo "❌ 无法提取有效宽度: $param_file (得到: $width)"
    continue
  fi

  # 从元数据文件读取高度（第 i+1 行）
  if [[ $i -ge $(wc -l < "$META_FILE") ]]; then
    echo "❌ 超出元数据范围: $ccitt_file"
    continue
  fi

  height=$(sed -n "$((i+1))p" "$META_FILE" | awk '{print $2}')
  if [[ -z "$height" || ! "$height" =~ ^[0-9]+$ ]]; then
    echo "❌ 无法提取有效高度: 行 $((i+1)) (得到: $height)"
    continue
  fi

  echo "📄 处理 $ccitt_file (宽度: ${width}, 高度: ${height})"

  # 转换：使用正确的 width 和 height
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
    continue
  fi

  # TIFF → WebP
  convert "/tmp/${base}.tiff" -define webp:lossless=true "$webp_file"
  rm -f "/tmp/${base}.tiff"

  echo "✅ 成功: $webp_file"
done
