#!/usr/bin/env python3
import os
import fitz
from PIL import Image
import io

ROOT = 'pdfs'
targets = ['001a.pdf', '001b.pdf', '001c.pdf', '001d.pdf', '001e.pdf']

for pdf_name in targets:
    pdf_path = os.path.join(ROOT, pdf_name)
    out_dir = os.path.join(ROOT, f"{os.path.splitext(pdf_name)[0]}_fixed")
    os.makedirs(out_dir, exist_ok=True)

    if not os.path.exists(pdf_path):
        print(f"❌ 文件不存在: {pdf_path}")
        continue

    print(f"\n📄 正在处理: {pdf_name}")
    doc = fitz.open(pdf_path)

    for page_idx in range(len(doc)):
        page = doc[page_idx]
        image_list = page.get_images(full=True)

        if not image_list:
            print(f"   ⚠️ 第 {page_idx+1} 页无图像")
            continue

        imgs = []
        for img in image_list:
            xref = img[0]
            try:
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                img_width = base_image["width"]
                img_height = base_image["height"]
                img_dpi = base_image.get("dpi", (96, 96))

                pil_img = Image.open(io.BytesIO(image_bytes))

                # --- 调试：打印原始信息 ---
                print(f"   🖼️  图像 {xref}: size={pil_img.size}, mode={pil_img.mode}")

                # 强制转为 RGB
                if pil_img.mode not in ['L', 'RGB']:
                    print(f"   🎨 转换模式: {pil_img.mode} → RGB")
                    pil_img = pil_img.convert('RGB')

                # 判断是否需要旋转（根据尺寸或模式）
                # 如果宽度 < 高度，可能是倒置的扫描页
                if pil_img.mode == 'RGB' and pil_img.width < pil_img.height * 1.2:
                    print(f"   🔁 旋转彩色图 180°: {pil_img.size}")
                    pil_img = pil_img.rotate(180, expand=False)
                    pil_img = pil_img.transpose(Image.FLIP_LEFT_RIGHT)

                if pil_img.size != (img_width, img_height):
                    pil_img = pil_img.resize((img_width, img_height), Image.NEAREST)

                imgs.append({
                    "img": pil_img,
                    "height": pil_img.height,
                    "width": pil_img.width
                })
            except Exception as e:
                print(f"   ❌ 提取失败 (xref={xref}): {e}")

        if not imgs:
            continue

        # 拼接
        total_height = sum(im["height"] for im in imgs)
        max_width = max(im["width"] for im in imgs)
        mode = imgs[0]["img"].mode
        bg_color = 255 if mode in ('L', 'RGB') else 0
        combined = Image.new(mode, (max_width, total_height), color=bg_color)

        y_offset = 0
        for im in imgs:
            combined.paste(im["img"], (0, y_offset))
            y_offset += im["img"].height
            im["img"].close()

        out_path = os.path.join(out_dir, f"{page_idx+1:03d}.png")
        combined.save(out_path, dpi=img_dpi)
        combined.close()
        print(f"   ✅ 保存: {out_path}")

    doc.close()
    print(f"🟢 {pdf_name} 处理完成")

print("\n🎉 所有 001 系列 PDF 已修复")
