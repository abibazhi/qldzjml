#!/usr/bin/env python3
import os
import sys
import subprocess
import tempfile
from PIL import Image

def main(pdf_path):
    if not os.path.isfile(pdf_path):
        print(f"错误：文件 '{pdf_path}' 不存在。", file=sys.stderr)
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmpdir:
        base = os.path.join(tmpdir, "img")
        # 直接提取为 PNG！
        try:
            subprocess.run(['pdfimages', '-png', pdf_path, base], check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print("pdfimages 失败:", e.stderr.decode(), file=sys.stderr)
            sys.exit(1)
        except FileNotFoundError:
            print("请安装 poppler-utils（含 pdfimages）", file=sys.stderr)
            sys.exit(1)

        # 获取图像列表（用于分页）
        try:
            list_out = subprocess.check_output(['pdfimages', '-list', pdf_path], text=True)
        except Exception as e:
            print("无法运行 pdfimages -list:", e, file=sys.stderr)
            sys.exit(1)

        pages = {}
        for line in list_out.splitlines()[2:]:
            toks = line.split()
            if len(toks) < 2:
                continue
            try:
                page = int(toks[0])
                seq = int(toks[1])
                pages.setdefault(page, []).append(seq)
            except ValueError:
                continue

        if not pages:
            print("未找到任何图像。")
            return

        # 按页拼接
        for page, seqs in sorted(pages.items()):
            images = []
            for seq in sorted(seqs):
                png_file = f"{base}-{seq-1:03d}.png"  # 注意：seq 从1开始，文件从0开始
                if not os.path.exists(png_file):
                    print(f"警告：{png_file} 不存在，跳过。", file=sys.stderr)
                    continue
                try:
                    img = Image.open(png_file).convert('RGB')  # 统一为 RGB
                    images.append(img)
                except Exception as e:
                    print(f"加载 {png_file} 失败: {e}", file=sys.stderr)
                    continue

            if not images:
                continue

            # 纵向拼接
            total_h = sum(im.height for im in images)
            max_w = max(im.width for im in images)
            full = Image.new('RGB', (max_w, total_h), (255, 255, 255))  # 白底
            y = 0
            for im in images:
                # 居中对齐（可选）
                x = (max_w - im.width) // 2
                full.paste(im, (x, y))
                y += im.height

            out_name = f"page-{page:03d}.png"
            full.save(out_name, dpi=(150, 150))  # 可设默认 DPI
            print(f"→ 已保存 {out_name}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("用法: python3 pdf2png_robust.py <input.pdf>")
        sys.exit(1)
    main(sys.argv[1])
