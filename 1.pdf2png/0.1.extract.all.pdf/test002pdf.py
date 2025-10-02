#!/usr/bin/env python3
import os, struct, subprocess, io

pdf   = 'pdfs/002.PDF'
out_dir = 'pdfs/002'
os.makedirs(out_dir, exist_ok=True)

# 1. 列出 pdfimages 发现 0 字节的碎片
print('=== 0 字节 PNG 列表 ===')
rows = subprocess.check_output(['pdfimages', '-list', pdf], text=True).splitlines()[2:]
for ln in rows:
    toks = ln.split()
    seq, w, h = int(toks[1]), int(toks[3]), int(toks[4])
    ccitt = f'{out_dir}/extract-{seq:03d}.ccitt'
    if os.path.isfile(ccitt) and os.path.getsize(ccitt) == 0:
        print(f'page {toks[0]}  seq {seq:02d}  0 字节')

# 2. 只抽第 2 页（num 1-15 → 文件 001-015）
print('=== 抽取第 2 页并合并 ===')
subprocess.run(['pdfimages', '-f', '2', '-l', '2', pdf, f'{out_dir}/p2'])
convert_cmd = ['convert'] + \
              [f'{out_dir}/p2-{i:03d}.jpg' for i in range(15)] + \
              [f'{out_dir}/page-2.jpg']
subprocess.run(convert_cmd)

print('完成：pdfs/002/page-2.jpg')
