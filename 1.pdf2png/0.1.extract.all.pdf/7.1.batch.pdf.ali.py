#!/usr/bin/env python3
import os, struct, subprocess, io, json
from PIL import Image

ROOT = 'pdfs'           # PDF 根目录
PROGRESS_FILE = 'progress.json'  # 断点记录

# ---------- 工具函数 ----------
def load_progress():
    return json.load(open(PROGRESS_FILE)) if os.path.exists(PROGRESS_FILE) else {}

def save_progress(p):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(p, f, indent=2)

def parse_pdfimages(pdf_path):
    """解析 pdfimages -list 输出，返回 fragment 列表"""
    cmd = ['pdfimages', '-list', pdf_path]
    try:
        raw = subprocess.check_output(cmd, text=True).splitlines()
    except subprocess.CalledProcessError as e:
        print(f"❌ 解析失败: {pdf_path}")
        return []
    
    # 跳过标题行
    rows = []
    for ln in raw[2:]:
        toks = ln.split()
        if len(toks) < 14:
            continue
        try:
            rows.append(dict(
                page=int(toks[0]),
                seq=int(toks[1]),
                w=int(toks[3]),
                h=int(toks[4]),
                dpi_x=int(toks[12]),
                dpi_y=int(toks[13])
            ))
        except (ValueError, IndexError):
            continue
    return rows

def ccitt_to_image(ccitt_path, width, height):
    """将 .ccitt 文件转为 PIL Image 对象"""
    try:
        with open(ccitt_path, 'rb') as f:
            data = f.read()
    except Exception as e:
        print(f"❌ 读取失败: {ccitt_path}")
        return None

    # 构造内存中的 TIFF
    tiff = bytearray()
    tiff.extend(b'II\x2a\x00')  # Little-endian TIFF
    tiff.extend(struct.pack('<I', 8))  # First IFD offset
    tiff.extend(struct.pack('<H', 5))  # 5 entries

    # Tags: Width, Height, Compression, StripOffsets, StripByteCounts
    tiff.extend(struct.pack('<HHII', 256, 4, 1, width))      # Width
    tiff.extend(struct.pack('<HHII', 257, 4, 1, height))     # Height
    tiff.extend(struct.pack('<HHII', 259, 3, 1, 4))          # Compression: CCITT Group 4
    tiff.extend(struct.pack('<HHII', 273, 4, 1, 8 + 2 + 5*12 + 4))  # StripOffsets
    tiff.extend(struct.pack('<HHII', 279, 4, 1, len(data)))  # StripByteCounts
    tiff.extend(b'\x00\x00\x00\x00')  # Next IFD
    tiff.extend(data)

    try:
        return Image.open(io.BytesIO(tiff))
    except Exception as e:
        print(f"❌ 解码失败: {ccitt_path}, {e}")
        return None

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
        print(f"📄 处理: {key}")

        # ===== 1. 解析 PDF 图像结构 =====
        rows = parse_pdfimages(pdf_path)
        if not rows:
            print(f"❌ 无图像或解析失败: {pdf_path}")
            progress[key] = 'failed'
            save_progress(progress)
            continue

        # ===== 2. 提取所有 CCITT 图像 =====
        tmp_prefix = os.path.join(out_dir, 'tmp')
        os.makedirs(out_dir, exist_ok=True)
        subprocess.run(['pdfimages', '-ccitt', pdf_path, tmp_prefix], 
                      check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # ===== 3. 按页分组并拼接 =====
        pages = {}
        for r in rows:
            pages.setdefault(r['page'], []).append(r)

        for page_num, fragments in pages.items():
            strip_images = []
            total_height = 0
            expected_width = fragments[0]['w']

            # 按 seq 排序，确保从上到下
            fragments.sort(key=lambda x: x['seq'])

            for frag in fragments:
                tmp_file = f"{tmp_prefix}-{frag['seq']:03d}.ccitt"
                if not os.path.exists(tmp_file):
                    print(f"⚠️ 缺失 fragment: {tmp_file}")
                    continue

                img = ccitt_to_image(tmp_file, frag['w'], frag['h'])
                if img is None:
                    continue

                # 宽度校验
                if img.width != expected_width:
                    print(f"⚠️ 宽度不一致: {tmp_file} ({img.width} != {expected_width})")
                
                strip_images.append(img)
                total_height += img.height

            # ===== 4. 拼接并保存完整页面 =====
            if strip_images:
                # 创建 1-bit 黑白图像
                dst = Image.new('1', (expected_width, total_height), color=1)  # 1=white
                y_offset = 0
                for img in strip_images:
                    dst.paste(img, (0, y_offset))
                    y_offset += img.height
                    img.close()  # 及时释放

                # 保存 PNG
                png_path = os.path.join(out_dir, f'{page_num}.png')
                dst.save(png_path, dpi=(fragments[0]['dpi_x'], fragments[0]['dpi_y']))
                dst.close()
                print(f"✅ 生成: {png_path} ({expected_width}x{total_height})")
            else:
                print(f"❌ 无法生成页面 {page_num}")

        # ===== 5. 清理临时文件 =====
        for frag in rows:
            tmp_file = f"{tmp_prefix}-{frag['seq']:03d}.ccitt"
            if os.path.exists(tmp_file):
                os.remove(tmp_file)

        # ===== 6. 标记完成 =====
        progress[key] = 'done'
        save_progress(progress)
        print(f"🟢 完成: {key}\n")

print("🎉 全部处理完毕")
