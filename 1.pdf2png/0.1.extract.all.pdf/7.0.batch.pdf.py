#!/usr/bin/env python3
import os, struct, subprocess, io, json
from PIL import Image

ROOT = 'pdfs'          # pdf 根目录
PROGRESS_FILE = 'progress.json'   # 断点记录

# ---------- 工具 ----------
def load_progress():
    return json.load(open(PROGRESS_FILE)) if os.path.exists(PROGRESS_FILE) else {}

def save_progress(p):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(p, f, indent=2)

def parse_pdfimages(pdf_path):
    cmd = ['pdfimages', '-list', pdf_path]
    raw = subprocess.check_output(cmd, text=True).splitlines()[2:]
    rows = []
    for ln in raw:
        toks = ln.split()
        rows.append(dict(
            page=int(toks[0]),
            seq=int(toks[1]),
            w=int(toks[3]),
            h=int(toks[4]),
            dpi_x=int(toks[12]),
            dpi_y=int(toks[13])))
    return rows

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

# ---------- 主流程 ----------
progress = load_progress()

for dirpath, _, filenames in os.walk(ROOT):
    for fname in sorted(filenames):
        if not fname.lower().endswith('.pdf'):
            continue
        pdf_path = os.path.join(dirpath, fname)
        base = os.path.splitext(fname)[0]
        out_dir = os.path.join(dirpath, base)

        key = os.path.relpath(pdf_path, ROOT)
        if progress.get(key) == 'done':
            print(f'[跳过] {key} 已完成')
            continue

        # 创建输出目录
        os.makedirs(out_dir, exist_ok=True)

        # 提取 CCITT
        rows = parse_pdfimages(pdf_path)
        subprocess.run(['pdfimages', '-all', pdf_path, os.path.join(out_dir, 'tmp')])

        # 按页合并并生成 1.png、2.png...
        pages = {}
        for r in rows:
            pages.setdefault(r['page'], []).append(r)

        for page_num, frags in sorted(pages.items()):
            strips = []
            for f in sorted(frags, key=lambda x: x['seq']):
                tmp = os.path.join(out_dir, f'tmp-{f["seq"]:03d}.ccitt')
                if not os.path.exists(tmp):
                    continue
                ccitt_to_png(tmp, f['w'], f['h'], f['dpi_x'], f['dpi_y'],
                             os.path.join(out_dir, f'{page_num}.png'))
            # 删除临时 CCITT
            for f in frags:
                tmp = os.path.join(out_dir, f'tmp-{f["seq"]:03d}.ccitt')
                os.remove(tmp) if os.path.exists(tmp) else None

        progress[key] = 'done'
        save_progress(progress)
        print(f'[完成] {key}')

print('全部处理完毕')
