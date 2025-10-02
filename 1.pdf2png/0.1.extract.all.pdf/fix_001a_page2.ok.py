#!/usr/bin/env python3
import fitz
from PIL import Image
import io
import os

PDF_PATH = "pdfs/001a.pdf"
PAGE_NUM = 2  # 第2页
OUTPUT_DIR = "test_page2"
os.makedirs(OUTPUT_DIR, exist_ok=True)

doc = fitz.open(PDF_PATH)
page = doc[PAGE_NUM - 1]

# --- 提取所有图像 fragment 及其位置 ---
fragments = []  # 存储 (img, x0, y0, x1, y1)
image_list = page.get_images(full=True)

for img in image_list:
    xref = img[0]
    try:
        # 获取图像的 bounding box
        rect_list = page.get_image_rects(xref)
        if not rect_list:
            continue
        # 通常只有一个 rect
        rect = rect_list[0]
        x0, y0, x1, y1 = rect.x0, rect.y0, rect.x1, rect.y1

        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        pil_img = Image.open(io.BytesIO(image_bytes))

        # 转 RGB
        if pil_img.mode not in ['RGB']:
            pil_img = pil_img.convert('RGB')

        # 关键：旋转 + 去镜像
        pil_img = pil_img.rotate(180, expand=False)
        pil_img = pil_img.transpose(Image.FLIP_LEFT_RIGHT)

        fragments.append({
            'img': pil_img,
            'x0': x0, 'y0': y0, 'x1': x1, 'y1': y1,
            'height': pil_img.height,
            'width': pil_img.width
        })
    except Exception as e:
        print(f"❌ 提取失败 {xref}: {e}")

if not fragments:
    print("❌ 未提取到图像")
    exit()

# --- 按 y0 排序（从上到下）---
fragments.sort(key=lambda f: f['y0'])
print(f"✅ 提取到 {len(fragments)} 个 fragment，按 y 坐标排序")

# --- 计算拼接尺寸 ---
total_height = sum(f['height'] for f in fragments)
max_width = max(f['width'] for f in fragments)  # 用于画布宽度

# 创建画布
combined = Image.new('RGB', (max_width, total_height), color=255)
y_offset = 0

for i, f in enumerate(fragments):
    w, h = f['width'], f['height']
    # 左对齐（你也可以改为居中：(max_width - w) // 2）
    x_offset = 0  # 左对齐
    # x_offset = (max_width - w) // 2  # 居中对齐

    combined.paste(f['img'], (x_offset, y_offset))
    print(f"📌 拼接 fragment {i+1}: {w}x{h} @ ({x_offset}, {y_offset})")
    y_offset += h
    f['img'].close()

# 保存
out_path = os.path.join(OUTPUT_DIR, "002_fixed.png")
combined.save(out_path, dpi=(140, 140))
print(f"\n✅ 修复完成: {out_path}")
doc.close()



# 假设 combined 是修复后的图像对象
# 计算裁剪区域，例如，如果你想裁剪掉右侧50像素：
left = 0
top = 0
right = combined.width - 379  # 调整这个值以决定裁剪多少
bottom = combined.height

# 裁剪图像
cropped_combined = combined.crop((left, top, right, bottom))
cropped_combined.show()  # 弹出预览

# 保存裁剪后的图像
out_path_cropped = os.path.join(OUTPUT_DIR, "002_fixed_cropped.png")
cropped_combined.save(out_path_cropped, dpi=(140, 140))
print(f"✅ 裁剪完成: {out_path_cropped}")

# 关闭所有打开的图像文件以释放资源
cropped_combined.close()
combined.close()

