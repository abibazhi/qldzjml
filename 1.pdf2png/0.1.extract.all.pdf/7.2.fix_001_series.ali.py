#!/usr/bin/env python3
import os, subprocess, json
from PIL import Image, ImageOps

ROOT = 'pdfs'
targets = ['001a.pdf', '001b.pdf', '001c.pdf', '001d.pdf', '001e.pdf']

def parse_pdfimages(pdf_path):
    """解析图像列表"""
    try:
        result = subprocess.run(
            ['pdfimages', '-list', pdf_path],
            capture_output=True, text=True, check=True
        )
        lines = result.stdout.splitlines()
        rows = []
        for ln in lines[2:]:
            toks = ln.split()
            if len(toks) < 14:
                continue
            try:
                rows.append({
                    'page': int(toks[0]),
                    'seq': int(toks[1]),
                    'width': int(toks[3]),
                    'height': int(toks[4]),
                    'enc': toks[8],
                    'dpi_x': int(toks[12]),
                    'dpi_y': int(toks[13])
                })
            except (ValueError, IndexError):
                continue
        return rows
    except subprocess.CalledProcessError as e:
        print(f"❌ pdfimages -list 失败: {e}")
        return []

# ---------- 主流程 ----------
for pdf_name in targets:
    pdf_path = os.path.join(ROOT, pdf_name)
    if not os.path.exists(pdf_path):
        print(f"❌ 文件不存在: {pdf_path}")
        continue

    print(f"\n📄 正在处理: {pdf_name}")
    base = os.path.splitext(pdf_name)[0]
    temp_dir = os.path.join(ROOT, base)
    temp_prefix = os.path.join(temp_dir, 'tmp')
    out_dir = os.path.join(ROOT, f"{base}_fixed")
    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    # 1. 解析结构
    fragments = parse_pdfimages(pdf_path)
    if not fragments:
        print(f"❌ 无法解析图像结构: {pdf_name}")
        continue

    # 2. 使用 -png 提取（更健壮）
    try:
        subprocess.run(
            ['pdfimages', '-png', pdf_path, 'tmp'],
            cwd=temp_dir,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"   ✅ 提取图像成功: {len(fragments)} 个 fragment")
    except subprocess.CalledProcessError:
        print(f"❌ pdfimages -png 提取失败，请检查 PDF 是否加密或损坏")
        continue

    # 3. 按页分组
    pages = {}
    for frag in fragments:
        pages.setdefault(frag['page'], []).append(frag)
    pages = dict(sorted(pages.items()))

    # 4. 处理每一页
    for page_num, frags in pages.items():
        frags = sorted(frags, key=lambda x: x['seq'])
        images = []
        total_height = 0
        target_width = frags[0]['width']

        for frag in frags:
            tmp_file = f"{temp_prefix}-{frag['seq']:03d}.png"
            if not os.path.exists(tmp_file):
                print(f"❌ 缺失文件: {tmp_file}")
                images = []
                break

            try:
                img = Image.open(tmp_file)
                img = ImageOps.exif_transpose(img)  # 校正方向
                if img.size != (frag['width'], frag['height']):
                    img = img.resize((frag['width'], frag['height']), Image.NEAREST)
                images.append(img)
                total_height += img.height
            except Exception as e:
                print(f"❌ 加载图像失败: {tmp_file}, {e}")
                images = []
                break

        if not images:
            print(f"❌ 无法生成页面 {page_num}")
            continue

        # 拼接
        if len(images) > 1:
            print(f"   🧩 拼接页面 {page_num}: {len(images)} 个 fragment")
            mode = images[0].mode
            bg = 255 if mode in ('L', 'RGB') else 0
            dst = Image.new(mode, (target_width, total_height), bg)
            y = 0
            for im in images:
                dst.paste(im, (0, y))
                y += im.height
                im.close()
        else:
            dst = images[0]

        # 保存
        out_path = os.path.join(out_dir, f"{page_num:03d}.png")
        dst.save(out_path, dpi=(frags[0]['dpi_x'], frags[0]['dpi_y']))
        dst.close()
        print(f"   ✅ 保存: {out_path}")

    print(f"🟢 {pdf_name} 处理完成")

print("\n🎉 所有 001 系列 PDF 已修复")
