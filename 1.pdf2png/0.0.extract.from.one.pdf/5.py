#!/usr/bin/env python3
import os, re, struct, sys
from PIL import Image

# 1. 读 pdfimages 列表
pdf = '038.pdf'
img_lst = os.popen(f'pdfimages -list {pdf}').read().splitlines()[2:]

# 2. 逐条处理
page_map = {}          # page -> [(seq, w, h, dpi_x, dpi_y)]
for ln in img_lst:
    page, seq, _, w, h, _, _, _, _, _, dpi_x, dpi_y, *_ = ln.split()
    page_map.setdefault(int(page), []).append((int(seq), int(w), int(h),
                                                int(dpi_x), int(dpi_y)))

# 3. 把每个 page 的碎片合成一张 PNG
for page, frags in sorted(page_map.items()):
    # 收集当前页所有碎片
    strips = []
    for seq, w, h, dpi_x, dpi_y in frags:
        ccitt_file = f'extract-{seq:03d}.ccitt'
        if not os.path.exists(ccitt_file):
            print(f'跳过缺失 {ccitt_file}')
            continue
        # 手工写 TIFF 头
        tiff = f'/tmp/{os.path.basename(ccitt_file)}.tiff'
        with open(ccitt_file, 'rb') as fin, open(tiff, 'wb') as fout:
            raw = fin.read()
            tiff_header = struct.pack(
                '<2sHIHHIIIIIIHHIIIIII',
                b'II', 42, 8,                  # TIFF 头
                14,                            # IFD 条目数
                256, 4, 1, w,                  # ImageWidth
                257, 4, 1, h,                  # ImageLength
                258, 3, 1, 1,                  # BitsPerSample
                259, 3, 1, 4,                  # Compression = CCITT Group 4
                262, 3, 1, 0,                  # Photometric = WhiteIsZero
                273, 4, 1, 8 + 14*12 + 4 + 4,  # StripOffsets
                278, 4, 1, h,                  # RowsPerStrip
                279, 4, 1, len(raw),           # StripByteCounts
                282, 5, 1, dpi_x * 100, 1,     # XResolution
                283, 5, 1, dpi_y * 100, 1,     # YResolution
                0, 0)                          # IFD 结束
            fout.write(tiff_header)
            fout.write(raw)
        img = Image.open(tiff)
        strips.append(img)

    # 纵向拼接
    if not strips:
        continue
    if len(strips) == 1:
        full = strips[0]
    else:
        full_w = strips[0].width
        full_h = sum(s.height for s in strips)
        full = Image.new('1', (full_w, full_h), 1)
        y = 0
        for s in strips:
            full.paste(s, (0, y))
            y += s.height

    out = f'page-{page:03d}.png'
    full.save(out, dpi=(dpi_x, dpi_y))
    print('生成', out)

# 4. 可选：合成 PDF
# os.system('convert page-*.png all_pages.pdf')
