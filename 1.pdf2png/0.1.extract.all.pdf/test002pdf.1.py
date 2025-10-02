#!/usr/bin/env python3
import os, struct, subprocess, io

pdf   = 'pdfs/002.PDF'
out_dir = 'pdfs/002'
os.makedirs(out_dir, exist_ok=True)

def ccitt_to_png(ccitt_path, w, h, dpi_x, dpi_y, out_path):
    if os.path.getsize(ccitt_path) == 0:
        print(f'[跳过] 空数据 {ccitt_path}')
        return
    with open(ccitt_path, 'rb') as f:
        data = f.read()
    tiff = bytearray()
    tiff.extend(b'II\x2a\x00')
    tiff.extend(struct.pack('<I', 8))
    tiff.extend(struct.pack('<H', 5))
    tiff.extend(struct.pack('<HHII', 256, 4, 1, w))
    tiff.extend(struct.pack('<HHII', 257, 4, 1, h))
    tiff.extend(struct.pack('<HHII', 259, 3, 1, 4))
    tiff.extend(struct.pack('<HHII', 273, 4, 1, 8 + 2 + 5 * 12 + 4))
    tiff.extend(struct.pack('<HHII', 279, 4, 1, len(data)))
    tiff.extend(b'\x00\x00\x00\x00')
    tiff.extend(data)
    img = Image.open(io.BytesIO(tiff))
    img.save(out_path, dpi=(dpi_x, dpi_y))

# 1. 只抽第 2 页（num 1-15）
subprocess.run(['pdfimages', '-f', '2', '-l', '2', pdf, f'{out_dir}/test'])
rows = subprocess.check_output(['pdfimages', '-list', pdf], text=True).splitlines()[2:]
rows = [ln.split() for ln in rows if int(ln.split()[0]) == 2]

# 2. 逐条处理并报告
for ln in rows:
    seq, w, h, dpi = int(ln[1]), int(ln[3]), int(ln[4]), int(ln[12])
    ccitt = f'{out_dir}/test-{seq:03d}.ccitt'
    png   = f'{out_dir}/page2-{seq:03d}.png'
    ccitt_to_png(ccitt, w, h, dpi, dpi, png)
    print(f'page2-{seq:03d}.png  大小: {os.path.getsize(png)} bytes')

print('测试完成，检查 pdfs/002/ 目录即可')
