#!/usr/bin/env python3
import os, struct, subprocess, io, sys
from PIL import Image

pdf = '038.pdf'

# 1. 拿 pdfimages 列表
txt = subprocess.check_output(['pdfimages', '-list', pdf], text=True)
head, *body = txt.splitlines()
cols = head.split()
rows = [dict(zip(cols, ln.split())) for ln in body]

# 2. 逐行处理

rows = [ln.split() for ln in txt.splitlines()[2:]]
for toks in rows:
    page  = int(toks[0])
    seq   = int(toks[1])
    w     = int(toks[3])
    h     = int(toks[4])
    dpi   = int(toks[8])

    ccitt = f'extract-{seq:03d}.ccitt'

    if not os.path.exists(ccitt):
        continue

    # 3. 构造最小 TIFF 头
    with open(ccitt, 'rb') as f:
        data = f.read()
    tiff = bytearray()
    tiff.extend(b'II\x2a\x00')                     # TIFF 头
    tiff.extend(struct.pack('<I', 8))              # IFD 偏移
    tiff.extend(struct.pack('<H', 5))              # 5 个标签
    tiff.extend(struct.pack('<HHII', 256, 4, 1, w))
    tiff.extend(struct.pack('<HHII', 257, 4, 1, h))
    tiff.extend(struct.pack('<HHII', 259, 3, 1, 4))  # G4
    tiff.extend(struct.pack('<HHII', 273, 4, 1, 8+2+5*12+4))
    tiff.extend(struct.pack('<HHII', 279, 4, 1, len(data)))
    tiff.extend(b'\x00\x00\x00\x00')               # IFD 结束
    tiff.extend(data)

    # 4. 转 PNG
    img = Image.open(io.BytesIO(tiff))
    out = f'page-{page:03d}.png'
    img.save(out, dpi=(dpi, dpi))
    print('→', out)

# 5. 可选：合成 PDF
# os.system('convert page-*.png all_pages.pdf')
