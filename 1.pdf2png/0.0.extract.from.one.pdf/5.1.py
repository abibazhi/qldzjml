#!/usr/bin/env python3
import os, subprocess
from PIL import Image

# 1. 拿 pdfimages 列表
pdf = '038.pdf'
lines = subprocess.check_output(['pdfimages', '-list', pdf],
                                text=True).splitlines()[2:]

# 2. 按页分组
pages = {}          # page -> [(seq, w, h, dpi)]
for ln in lines:
    toks = ln.split()
    page, seq = int(toks[0]), int(toks[1])
    w, h, dpi = int(toks[3]), int(toks[4]), int(toks[8])
    pages.setdefault(page, []).append((seq, w, h, dpi))

# 3. 逐页处理
for page, frags in sorted(pages.items()):
    strips = []
    for seq, w, h, dpi in frags:
        ccitt = f'extract-{seq:03d}.ccitt'
        # Pillow 可以直接读“类 TIFF”的裸 G4，只需告诉它尺寸
        im = Image.frombytes('1', (w, h),
                             open(ccitt, 'rb').read(),
                             decoder_name='group4')
        strips.append(im)

    # 纵向拼接
    if len(strips) == 1:
        full = strips[0]
    else:
        total_h = sum(s.height for s in strips)
        full = Image.new('1', (strips[0].width, total_h))
        y = 0
        for s in strips:
            full.paste(s, (0, y))
            y += s.height

    out = f'page-{page:03d}.png'
    full.save(out, dpi=(dpi, dpi))
    print('→', out)

# 4. 可选：合成 PDF
# os.system('convert page-*.png all_pages.pdf')
