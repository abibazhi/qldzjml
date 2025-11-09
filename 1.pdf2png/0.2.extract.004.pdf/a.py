#!/usr/bin/env python3
import os
import sys
import subprocess
import struct
import io
import tempfile
from PIL import Image

def ccitt_to_pil(ccitt_data, width, height):
    """将原始 CCITT 数据包装为最小 TIFF，供 Pillow 读取"""
    # TIFF header (little-endian)
    tiff = bytearray(b'II\x2a\x00')          # little-endian, magic
    tiff.extend(struct.pack('<I', 8))        # offset to IFD
    tiff.extend(struct.pack('<H', 5))        # number of tags

    # ImageWidth
    tiff.extend(struct.pack('<HHII', 256, 4, 1, width))
    # ImageLength
    tiff.extend(struct.pack('<HHII', 257, 4, 1, height))
    # Compression (4 = CCITT Group 4)
    tiff.extend(struct.pack('<HHII', 259, 3, 1, 4))
    # StripOffsets
    strip_offset = 8 + 2 + 5 * 12 + 4
    tiff.extend(struct.pack('<HHII', 273, 4, 1, strip_offset))
    # StripByteCounts
    tiff.extend(struct.pack('<HHII', 279, 4, 1, len(ccitt_data)))
    # IFD terminator
    tiff.extend(b'\x00\x00\x00\x00')
    # Raw CCITT data
    tiff.extend(ccitt_data)

    return Image.open(io.BytesIO(tiff))

def main(pdf_path):
    if not os.path.isfile(pdf_path):
        print(f"错误：文件 '{pdf_path}' 不存在。", file=sys.stderr)
        sys.exit(1)

    # 创建临时目录存放 extract-*.ccitt
    with tempfile.TemporaryDirectory() as tmpdir:
        base = os.path.join(tmpdir, "extract")
        try:
            # 提取所有 CCITT 图像
            subprocess.run(['pdfimages', '-ccitt', pdf_path, base], check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print("pdfimages 执行失败:", e.stderr.decode(), file=sys.stderr)
            sys.exit(1)
        except FileNotFoundError:
            print("错误：未找到 'pdfimages' 命令，请安装 poppler-utils（如 apt install poppler-utils 或 brew install poppler）", file=sys.stderr)
            sys.exit(1)

        # 获取图像列表
        try:
            list_out = subprocess.check_output(['pdfimages', '-list', pdf_path], text=True)
        except Exception as e:
            print("无法读取 pdfimages -list:", e, file=sys.stderr)
            sys.exit(1)

        lines = list_out.splitlines()[2:]  # 跳过标题行
        pages = {}

        for ln in lines:
            toks = ln.split()
            if len(toks) < 14:
                continue
            try:
                page = int(toks[0])
                seq = int(toks[1])
                w = int(toks[3])
                h = int(toks[4])
                dpi_x = int(toks[12])
                dpi_y = int(toks[13])
                pages.setdefault(page, []).append((seq, w, h, dpi_x, dpi_y))
            except (ValueError, IndexError):
                continue

        if not pages:
            print("警告：未在 PDF 中找到任何可提取的图像。")
            return

        # 按页处理
        for page, frags in sorted(pages.items()):
            strips = []
            for seq, w, h, dpi_x, dpi_y in sorted(frags, key=lambda x: x[0]):
                ccitt_file = f"{base}-{seq-1:03d}.ccitt"  # 注意：seq 从1开始，文件从0开始
                if not os.path.exists(ccitt_file):
                    print(f"警告：缺失文件 {ccitt_file}，跳过。", file=sys.stderr)
                    continue
                with open(ccitt_file, 'rb') as f:
                    data = f.read()
                try:
                    img = ccitt_to_pil(data, w, h)
                    strips.append((img, dpi_x, dpi_y))
                except Exception as e:
                    print(f"解码 {ccitt_file} 失败: {e}", file=sys.stderr)
                    continue

            if not strips:
                continue

            # 使用第一页的 DPI
            dpi_x, dpi_y = strips[0][1], strips[0][2]
            total_h = sum(img.height for img, _, _ in strips)
            width = strips[0][0].width
            full = Image.new('1', (width, total_h), 1)
            y = 0
            for img, _, _ in strips:
                full.paste(img, (0, y))
                y += img.height

            out_name = f"page-{page:03d}.png"
            full.save(out_name, dpi=(dpi_x, dpi_y))
            print(f"→ 已保存 {out_name}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("用法: python3 pdf2png.py <input.pdf>")
        sys.exit(1)
    main(sys.argv[1])
