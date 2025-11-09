#!/usr/bin/env python3
import os, struct, subprocess, io
from PIL import Image

pdf = '038.pdf'
#pdf = '004.pdf'

# 读取 pdfimages 列表
lines = subprocess.check_output(['pdfimages', '-list', pdf], text=True).splitlines()[2:]

# 先把所有碎片按 page 分组
pages = {}
for ln in lines:
    toks = ln.split()
    page  = int(toks[0])
    seq   = int(toks[1])
    w     = int(toks[3])
    h     = int(toks[4])
    dpi_x = int(toks[12])
    dpi_y = int(toks[13])
    pages.setdefault(page, []).append((seq, w, h, dpi_x, dpi_y))

# 逐页处理
for page, frags in sorted(pages.items()):
    strips = []
    for seq, w, h, dpi_x, dpi_y in sorted(frags, key=lambda x: x[0]):
        ccitt = f'extract-{seq:03d}.ccitt'
        if not os.path.exists(ccitt):
            continue
        # 构造最小 TIFF
        with open(ccitt, 'rb') as f:
            data = f.read()
        tiff = bytearray()
        tiff.extend(b'II\x2a\x00')
        tiff.extend(struct.pack('<I', 8))
        tiff.extend(struct.pack('<H', 5))
        tiff.extend(struct.pack('<HHII', 256, 4, 1, w))
        tiff.extend(struct.pack('<HHII', 257, 4, 1, h))
        tiff.extend(struct.pack('<HHII', 259, 3, 1, 4))
        tiff.extend(struct.pack('<HHII', 273, 4, 1, 8+2+5*12+4))
        tiff.extend(struct.pack('<HHII', 279, 4, 1, len(data)))
        tiff.extend(b'\x00\x00\x00\x00')
        tiff.extend(data)

        # Pillow 解码
        img = Image.open(io.BytesIO(tiff))
        strips.append(img)

    if not strips:
        continue

    # 纵向拼成整页
    total_h = sum(s.height for s in strips)
    full = Image.new('1', (strips[0].width, total_h), 1)
    y = 0
    for s in strips:
        full.paste(s, (0, y))
        y += s.height

    out = f'page-{page:03d}.png'
    full.save(out, dpi=(dpi_x, dpi_y))
    print('→', out)
