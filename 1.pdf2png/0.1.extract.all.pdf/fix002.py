#!/usr/bin/env python3
import os, struct, subprocess, io

pdf   = 'pdfs/002.PDF'
out_dir = 'pdfs/002'
os.makedirs(out_dir, exist_ok=True)

# ---------- 工具 ----------
def ccitt_to_png(ccitt_path, w, h, dpi_x, dpi_y, out_path):
    with open(ccitt_path, 'rb') as f:
        data = f.read()
    if len(data) == 0:
        print(f'[跳过] 空数据 {ccitt_path}')
        return
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
    Image.open(io.BytesIO(tiff)).save(out_path, dpi=(dpi_x, dpi_y))

# ---------- 主流程 ----------
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
    if os.path.isfile(png_file) and os.path.getsize(png_file) > 0:
        print(f'[跳过] page-{page_num}.png 已正常')
        continue

    # 重新抽该单页
    subprocess.run(['pdfimages', '-f', str(page_num), '-l', str(page_num),
                    pdf, os.path.join(out_dir, 'tmp_re')])
    ccitt = os.path.join(out_dir, 'tmp_re-000.ccitt')
    if not os.path.exists(ccitt):
        print(f'[警告] 无数据 page-{page_num}')
        continue

    seq, w, h, dpi = frags[0]
    ccitt_to_png(ccitt, w, h, dpi, dpi, png_file)
    os.remove(ccitt)
    print(f'[完成] page-{page_num}.png')

print('002.pdf 处理完毕')
