#!/usr/bin/env python3
import os, struct, subprocess, io, json
from PIL import Image

ROOT          = 'pdfs'
PROGRESS_FILE = 'progress.json'

def load_progress():
    return json.load(open(PROGRESS_FILE)) if os.path.exists(PROGRESS_FILE) else {}

def save_progress(p):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(p, f, indent=2)

def parse_pdfimages(pdf_path):
    raw = subprocess.check_output(['pdfimages', '-list', pdf_path], text=True).splitlines()[2:]
    pages = {}
    for ln in raw:
        toks = ln.split()
        page = int(toks[0])
        seq  = int(toks[1])
        w    = int(toks[3])
        h    = int(toks[4])
        dpi  = int(toks[12])
        pages.setdefault(page, []).append((seq, w, h, dpi))
    return pages

def ccitt_to_png(ccitt_path, w, h, dpi_x, dpi_y, out_path):
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
    Image.open(io.BytesIO(tiff)).save(out_path, dpi=(dpi_x, dpi_y))

progress = load_progress()

for dirpath, _, filenames in os.walk(ROOT):
    for fname in sorted(filenames):
        if not fname.lower().endswith('.pdf'):
            continue
        pdf_path = os.path.join(dirpath, fname)
        base     = os.path.splitext(fname)[0]
        out_dir  = os.path.join(dirpath, base)
        key      = os.path.relpath(pdf_path, ROOT)

        # 跳过已完成且无 0 字节 PNG 的
        if progress.get(key) == 'done' and not any(
            os.path.isfile(p) and os.path.getsize(p) == 0
            for p in os.listdir(out_dir) if p.endswith('.png')
        ):
            print(f'[跳过] {key} 已完成且无 0 字节 PNG')
            continue

        os.makedirs(out_dir, exist_ok=True)
        pages = parse_pdfimages(pdf_path)

        # 按需抽取整本或单页
        need_all = (progress.get(key) != 'done')
        if need_all:
            subprocess.run(['pdfimages', '-all', pdf_path, os.path.join(out_dir, 'tmp')])
            progress[key] = 'done'
            save_progress(progress)

        # 生成/修复 PNG
        for page_num, frags in sorted(pages.items()):
            out_png = os.path.join(out_dir, f'{page_num}.png')
            if os.path.isfile(out_png) and os.path.getsize(out_png) > 0:
                continue  # 已正常

            subprocess.run([
                'pdfimages', '-f', str(page_num), '-l', str(page_num),
                pdf_path, os.path.join(out_dir, 'tmp_re')
            ])
            tmp_ccitt = os.path.join(out_dir, 'tmp_re-000.ccitt')
            if not os.path.exists(tmp_ccitt):
                continue

            seq, w, h, dpi = frags[0]
            ccitt_to_png(tmp_ccitt, w, h, dpi, dpi, out_png)
            os.remove(tmp_ccitt)

        print(f'[完成] {key}')

print('全部处理完毕')
