#!/bin/bash
for ccitt in 038-*.ccitt; do
  base=$(basename "$ccitt" .ccitt)
  params="${base}.params"
  width=$(grep -oE '-X [0-9]+' "$params" | cut -d' ' -f2)

  convert -depth 1 -colorspace Gray -monochrome \
          "${ccitt}[${width}x]" \
          -define webp:lossless=true \
          -define webp:method=6 \
          -define webp:auto-filter=true \
          "${base}.webp"

  echo "✅ $ccitt → ${base}.webp"
done
