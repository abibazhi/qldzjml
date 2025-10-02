#!/usr/bin/env python3
import os, subprocess, re
from PIL import Image

pdf = '038.pdf'

# 1. 用 pdfimages 拿列表
lines = subprocess.check_output(['pdfimages', '-list', pdf],
                                text=True).splitlines()

# 2. 把表头去掉，逐行解析成 dict
cols = lines[0].split()
rows = [dict(zip(cols, ln.split())) for ln in lines[2:]]

# 3. 按页分组
pages = {}
for r in rows:
    page   = int(r['page'])
    num    = int(r['num'])
    width  = int(r['width'])
    height = int(r['height'])
    dpi_x  = int(r['x-ppi'])
    pages.setdefault(page, []).append((num, width, height, dpi_x))

# 4. 逐页处理
for page, frags in sorted(pages.items()):
    strips = []
    for num, w, h, dpi in frags:
        ccitt = f'extract-{num:03d}.ccitt'
        if not os.path.exists(ccitt):
            print('跳过缺失', ccitt)
            continue
        # Pillow 直接解码裸 G4
        img = Image.frombytes('1', (w, h),
                              open(ccitt, 'rb').read(),
                              'raw', '1', 0, 1)   # 关键参数
        strips.append(img)

    # 纵向拼接
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

# 5. 可选：整本 PDF
# os.system('convert page-*.png all_pages.pdf')
