#!/usr/bin/env python3
import fitz
from PIL import Image, ImageOps
import io
import os

# --- 配置 ---
PDF_PATH = "pdfs/001a.pdf"        # 输入 PDF
PAGE_NUM = 1                      # 测试第几页（从1开始）
OUTPUT_DIR = "test_output"        # 输出目录
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- 调整开关（手动修改这里测试不同效果）---
ROTATE_180 = True        # 是否旋转 180°（解决上下颠倒）
FLIP_LEFT_RIGHT = True  # 是否水平翻转（解决左右镜像）
CONVERT_RGB = True       # 是否转为 RGB
# --------------------------------------------------

print(f"📄 打开: {PDF_PATH}")
doc = fitz.open(PDF_PATH)

if PAGE_NUM > len(doc):
    print(f"❌ 页数超出范围！PDF 只有 {len(doc)} 页")
    exit(1)

page = doc[PAGE_NUM - 1]
image_list = page.get_images(full=True)

if not image_list:
    print(f"❌ 第 {PAGE_NUM} 页无图像")
    exit(1)

print(f"🖼️  第 {PAGE_NUM} 页找到 {len(image_list)} 个图像 fragment")

for idx, img in enumerate(image_list):
    xref = img[0]
    base_image = doc.extract_image(xref)
    image_bytes = base_image["image"]
    width = base_image["width"]
    height = base_image["height"]
    ext = base_image["ext"]

    pil_img = Image.open(io.BytesIO(image_bytes))
    print(f"  🔹 fragment {idx+1}: {width}x{height}, mode={pil_img.mode}, format={ext}")

    # --- 转换模式 ---
    if CONVERT_RGB and pil_img.mode not in ['L', 'RGB']:
        print(f"     → 转换模式: {pil_img.mode} → RGB")
        pil_img = pil_img.convert('RGB')

    # --- 旋转 180° ---
    if ROTATE_180:
        print(f"     → 旋转 180°")
        pil_img = pil_img.rotate(180, expand=False)

    # --- 水平翻转（镜像）---
    if FLIP_LEFT_RIGHT:
        print(f"     → 水平翻转（左右镜像）")
        pil_img = pil_img.transpose(Image.FLIP_LEFT_RIGHT)

    # --- 保存单个 fragment（用于调试）---
    frag_path = os.path.join(OUTPUT_DIR, f"frag_{PAGE_NUM}_{idx+1}.png")
    pil_img.save(frag_path)
    print(f"     → 保存: {frag_path}")

    # --- 显示图像（如果你有 GUI）---
    # pil_img.show(title=f"Page {PAGE_NUM} - Fragment {idx+1}")

    # 只测试第一个 fragment（通常是主图）
    break

# --- 拼接所有 fragment ---
if len(image_list) > 1:
    print("💡 正在拼接所有 fragment...")
    imgs = []
    total_height = 0
    max_width = 0

    for img in image_list:
        xref = img[0]
        base_image = doc.extract_image(xref)
        pil_img = Image.open(io.BytesIO(base_image["image"]))

        if CONVERT_RGB and pil_img.mode not in ['L', 'RGB']:
            pil_img = pil_img.convert('RGB')

        if ROTATE_180:
            pil_img = pil_img.rotate(180, expand=False)

        if FLIP_LEFT_RIGHT:
            pil_img = pil_img.transpose(Image.FLIP_LEFT_RIGHT)

        pil_img = pil_img.resize((base_image["width"], base_image["height"]), Image.NEAREST)
        imgs.append(pil_img)
        total_height += pil_img.height
        max_width = max(max_width, pil_img.width)

    # 拼接
    mode = imgs[0].mode
    bg = 255 if mode in ('L', 'RGB') else 0
    combined = Image.new(mode, (max_width, total_height), bg)
    y = 0
    for im in imgs:
        combined.paste(im, (0, y))
        y += im.height
        im.close()

    # 保存拼接图
    combined_path = os.path.join(OUTPUT_DIR, f"combined_page_{PAGE_NUM}.png")
    combined.save(combined_path)
    print(f"✅ 拼接完成: {combined_path}")
    # combined.show()  # 弹出预览

doc.close()
print(f"\n🎉 测试完成！查看 '{OUTPUT_DIR}' 目录")
