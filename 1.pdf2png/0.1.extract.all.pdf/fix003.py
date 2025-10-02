#!/usr/bin/env python3
import os, struct, subprocess, io

pdf   = 'pdfs/002.PDF'
out_dir = 'pdfs/002'
os.makedirs(out_dir, exist_ok=True)

# 工具：跳过 <1 KB
def ccitt_to_png(ccitt_path, w, h, dpi_x, dpi_y, out_path):
    if os.path.getsize(ccitt_path) < 1024:
        print(f'[跳过] 数据<1K {ccitt_path}')
        return
    with open(ccitt_path, 'rb') as f:
        data = f.read()
    tiff = bytearray()
    # …（同上，略）
    Image.open(io.BytesIO(tiff)).save(out_path, dpi=(dpi_x, dpi_y))

# 主流程：只处理 002.pdf
pages = {}
for ln in subprocess.check_output(['pdfimages', '-list', pdf], text=True).splitlines()[2:]:
    toks = ln.split()
    page = int(toks[0])
    seq  = int(toks[1])
    w    = int(toks[3])
    h    = int(toks[4])
    dpi  = int(toks[12])
    pages.setdefault(page, []).append((seq, w, h, dpi))

for page_num, frags in sorted(pages.items()):
    png_file = os.path.join(out_dir, f'{page_num}.png')
    if os.path.isfile(png_file) and os.path.getsize(png_file) >= 1024:
        print(f'[跳过] page-{page_num}.png ≥1KB')
        continue

    subprocess.run(['pdfimages', '-f', str(page_num), '-l', str(page_num),
                    pdf, os.path.join(out_dir, 'tmp_re')])
    ccitt = os.path.join(out_dir, 'tmp_re-000.ccitt')
    if not os.path.exists(ccitt):
        continue
    seq, w, h, dpi = frags[0]
    ccitt_to_png(ccitt, w, h, dpi, dpi, png_file)
    os.remove(ccitt)
    print(f'[完成] page-{page_num}.png')

print('002.pdf 已按 <1KB 阈值修复完毕')
