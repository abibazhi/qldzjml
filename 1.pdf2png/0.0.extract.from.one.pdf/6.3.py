#!/usr/bin/env python3
import os, re, struct, subprocess, io
from PIL import Image

pdf = '038.pdf'

# 1. 拿列表，逐行正则解析
rows = []
pat = re.compile(
    r'^\s*(?P<page>\d+)\s+(?P<num>\d+)\s+\S+\s+(?P<w>\d+)\s+(?P<h>\d+)\s+\S+\s+\S+\s+\S+\s+\S+\s+(?P<xppi>\d+)\s+(?P<yppi>\d+)'
)
for ln in subprocess.check_output(['pdfimages', '-list', pdf], text=True).splitlines():
    m = pat.match(ln)
    if m:
        rows.append(m.groupdict())

# 2. 逐行处理
for r in rows:
    page  = int(r['page'])
    seq   = int(r['num'])
    w     = int(r['w'])
    h     = int(r['h'])
    dpi_x = int(r['xppi'])
    dpi_y = int(r['yppi'])

    ccitt = f'extract-{seq:03d}.ccitt'
    if not os.path.exists(ccitt):
        continue

    # 3. 构造最小 TIFF 头
    with open(ccitt, 'rb') as f:
        data = f.read()
    tiff = bytearray()
    tiff.extend(b'II\x2a\x00')          # TIFF 头
    tiff.extend(struct.pack('<I', 8))   # IFD 偏移
    tiff.extend(struct.pack('<H', 5))
    tiff.extend(struct.pack('<HHII', 256, 4, 1, w))
    tiff.extend(struct.pack('<HHII', 257, 4, 1, h))
    tiff.extend(struct.pack('<HHII', 259, 3, 1, 4))  # G4
    tiff.extend(struct.pack('<HHII', 273, 4, 1, 8 + 2 + 5 * 12 + 4))
    tiff.extend(struct.pack('<HHII', 279, 4, 1, len(data)))
    tiff.extend(b'\x00\x00\x00\x00')
    tiff.extend(data)

    # 4. 转 PNG
    img = Image.open(io.BytesIO(tiff))
    out = f'page-{page:03d}.png'
    img.save(out, dpi=(dpi_x, dpi_y))
    print('→', out)
