#!/usr/bin/env python3
"""
把 pdfimages 抽出的 extract-*.ccitt 还原成整页 PNG
用法: python ccitt2png_fix.py
"""
import os, struct, subprocess
from PIL import Image

pdf = '038.pdf'

# 1. 获取 pdfimages 列表
txt = subprocess.check_output(['pdfimages', '-list', pdf], text=True)
head, *body = txt.splitlines()
cols = head.split()
rows = [dict(zip(cols, ln.split())) for ln in body]

# 2. 按页分组
pages = {}
for r in rows:
    page  = int(r['page'])
    seq   = int(r['num'])
    w     = int(r['width'])
    h     = int(r['height'])
    dpi_x = int(r['x-ppi'])
    pages.setdefault(page, []).append((seq, w, h, dpi_x))

# 3. 把裸 CCITT 包装成 TIFF，再转 PNG
for page, frags in sorted(pages.items()):
    strips = []
    for seq, w, h, dpi in frags:
        ccitt_path = f'extract-{seq:03d}.ccitt'
        if not os.path.exists(ccitt_path):
            print('跳过缺失', ccitt_path)
            continue

        # --- 构造最小 TIFF ---
        with open(ccitt_path, 'rb') as f:
            data = f.read()

        tiff = bytearray()
        # TIFF 头
        tiff.extend(struct.pack('<2sHI', b'II', 42, 8))
        # IFD 条目数
        tiff.extend(struct.pack('<H', 9))
        # IFD 内容（标签, 类型, 计数, 值/偏移）
        entries = [
            (256, 4, 1, w),                         # width
            (257, 4, 1, h),                         # height
            (258, 3, 1, 1),                         # BitsPerSample
            (259, 3, 1, 4),                         # Compression=CCITT Group4
            (262, 3, 1, 0),                         # Photometric=WhiteIsZero
            (273, 4, 1, 8 + 2 + 9*12 + 4),          # StripOffsets
            (278, 4, 1, h),                         # RowsPerStrip
            (279, 4, 1, len(data)),                 # StripByteCounts
            (282, 5, 1, dpi*100, 1),                # XResolution
            (283, 5, 1, dpi*100, 1),                # YResolution
        ]
        for tag, typ, cnt, *val in entries:
            if len(val) == 2:
                tiff.extend(struct.pack('<HHII', tag, typ, cnt, val[0]))
                tiff.extend(struct.pack('<I', val[1]))
            else:
                tiff.extend(struct.pack('<HHI', tag, typ, cnt))
                tiff.extend(struct.pack('<I', val[0]))
        tiff.extend(b'\0\0\0\0')                   # IFD 结束
        tiff.extend(data)                          # 真正的 CCITT 数据

        # 4. Pillow 打开并转 PNG
        img = Image.open(io.BytesIO(tiff))
        strips.append(img)

    # 5. 纵向拼接
    if not strips:
        continue
    if len(strips) == 1:
        full = strips[0]
    else:
        total_h = sum(s.height for s in strips)
        full = Image.new('1', (strips[0].width, total_h), 1)
        y = 0
        for s in strips:
            full.paste(s, (0, y))
            y += s.height

    out = f'page-{page:03d}.png'
    full.save(out, dpi=(dpi, dpi))
    print('→', out)

# 6. 可选：整本 PDF
# os.system('convert page-*.png all_pages.pdf')
