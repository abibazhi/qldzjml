#!/bin/bash

for ccitt_file in 038-*.ccitt; do
  base=$(basename "$ccitt_file" .ccitt)
  param_file="${base}.params"
  tiff_file="/tmp/${base}.tiff"
  webp_file="${base}.webp"

  # 检查参数文件
  if [[ ! -f "$param_file" ]]; then
    echo "❌ 缺少参数文件: $param_file"
    continue
  fi

  # 提取宽度（兼容性强）
  width=$(awk '{for(i=1;i<=NF;i++) if($i=="-X") print $(i+1); exit}' "$param_file")
  if [[ -z "$width" ]]; then
    echo "❌ 无法提取宽度: $param_file"
    continue
  fi

  echo "📄 处理 $ccitt_file (宽度: ${width})"

  # 第一步：将原始 .ccitt 数据转为 TIFF
  convert \
    -depth 1 \
    -colorspace Gray \
    -monochrome \
    -define tiff:fill-order=msb \
    -compress Group4 \
    -size ${width}x1 \
    "ccitt:$ccitt_file" \
    "$tiff_file" 2>/dev/null

  if [[ $? -ne 0 ]]; then
    echo "❌ 转换失败: $ccitt_file"
    continue
  fi

  # 第二步：TIFF → WebP
  convert "$tiff_file" -define webp:lossless=true "$webp_file"

  # 清理临时 TIFF
  rm -f "$tiff_file"

  echo "✅ 成功: $webp_file"
done
