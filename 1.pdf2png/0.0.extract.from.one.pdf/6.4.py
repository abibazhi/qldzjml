#!/usr/bin/env python3
"""
把当前目录下所有 extract-*.ccitt 一次性转成 PNG
（列号写法：page=0, num=1, width=3, height=4, x-ppi=9, y-ppi=10）
"""
import os, struct, subprocess, io
from PIL import Image

pdf = '038.pdf'

# 1. 拿 pdfimages 列表
lines = subprocess.check_output(['pdfimages', '-list', pdf], text=True).splitlines()[2:]

for ln in lines:
    toks = ln.split()
    page  = int(toks[0])
    seq   = int(toks[1])
    w     = int(toks[3])
    h     = int(toks[4])
    dpi_x = int(toks[9])
    dpi_y = int(toks[10])

    ccitt = f'extract-{seq:03d}.ccitt'
    if not os.path.exists(ccitt):
        continue

    # 2. 构造最小 TIFF
    with open(ccitt, 'rb') as f:
        data = f.read()
    tiff = bytearray()
    tiff.extend(b'II\x2a\x00')                # TIFF 头
    tiff.extend(struct.pack('<I', 8))         # IFD 偏移
    tiff.extend(struct.pack('<H', 5))         # 5 个标签
    tiff.extend(struct.pack('<HHII', 256, 4, 1, w))  # ImageWidth
    tiff.extend(struct.pack('<HHII', 257, 4, 1, h))  # ImageLength
    tiff.extend(struct.pack('<HHII', 259, 3, 1, 4))  # Compression = G4
    tiff.extend(struct.pack('<HHII', 273, 4, 1, 8+2+5*12+4))  # StripOffsets
    tiff.extend(struct.pack('<HHII', 279, 4, 1, len(data)))  # StripByteCounts
    tiff.extend(b'\x00\x00\x00\x00')          # IFD 结束
    tiff.extend(data)

    # 3. Pillow 打开并转 PNG
    img = Image.open(io.BytesIO(tiff))
    out = f'page-{page:03d}.png'
    img.save(out, dpi=(dpi_x, dpi_y))
    print('→', out)
