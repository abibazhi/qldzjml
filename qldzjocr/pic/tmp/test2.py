import paddleocr
from PIL import Image, ImageDraw

# 初始化 PaddleOCR，仅启用文本检测，禁用文字识别
ocr = paddleocr.PaddleOCR(use_angle_cls=True, lang="ch", det=True, rec=False)

# 要分析的图片路径
img_path = 'qldzjpng/001/167.png'

# 执行版面分析（仅检测文本块）
result = ocr.ocr(img_path, cls=True)

# 打印文本块位置信息
for idx, line in enumerate(result):
    print(f"Text Block {idx + 1} Coordinates: ", line[0])  # 输出每个文本块的坐标

# 可选：可视化输出，绘制文本框
image = Image.open(img_path).convert('RGB')
draw = ImageDraw.Draw(image)
for idx, line in enumerate(result):
    points = line[0]  # 文本块的四个角点坐标
    # 将坐标展平成一个简单的列表
    flat_points = [coord for point in points for coord in point]
    draw.polygon(flat_points, outline="red")
    draw.text((flat_points[0], flat_points[1]), str(idx + 1), fill="red")  # 在每个文本块左上角标注序号

# 保存或显示带有文本框标记的图片
image.save("output_with_boxes.jpg")
image.show()
