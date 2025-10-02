#!/usr/bin/env python3
import os
import fitz  # pip install PyMuPDF

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

        # 通常每页一个图像（或多个拼接条带）
        imgs = []
        for img in image_list:
            xref = img[0]
            try:
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                img_width = base_image["width"]
                img_height = base_image["height"]
                img_dpi = base_image.get("dpi", (96, 96))  # 默认 96 DPI

                # 转为 PIL.Image 并校正方向
                from PIL import Image, ImageOps
                import io
                pil_img = Image.open(io.BytesIO(image_bytes))
                pil_img = ImageOps.exif_transpose(pil_img)

                # 强制尺寸匹配
                if pil_img.size != (img_width, img_height):
                    pil_img = pil_img.resize((img_width, img_height), Image.NEAREST)

                imgs.append({
                    "img": pil_img,
                    "height": pil_img.height,
                    "width": pil_img.width
                })
            except Exception as e:
                print(f"   ❌ 提取图像失败 (xref={xref}): {e}")

        if not imgs:
            continue

        # 拼接多 fragment（按宽度排序，假设是纵向分割）
        imgs.sort(key=lambda x: x["width"], reverse=True)  # 宽的在前（主图）
        total_height = sum(im["height"] for im in imgs)
        max_width = max(im["width"] for im in imgs)

        # 创建拼接图像
        mode = imgs[0]["img"].mode
        bg_color = 255 if mode in ('L', 'RGB') else 0
        combined = Image.new(mode, (max_width, total_height), color=bg_color)
        y_offset = 0
        for im in imgs:
            combined.paste(im["img"], (0, y_offset))
            y_offset += im["img"].height
            im["img"].close()

        # 保存
        out_path = os.path.join(out_dir, f"{page_idx+1:03d}.png")
        combined.save(out_path, dpi=img_dpi)
        combined.close()
        print(f"   ✅ 保存: {out_path}")

    doc.close()
    print(f"🟢 {pdf_name} 处理完成")

print("\n🎉 所有 001 系列 PDF 已修复")
