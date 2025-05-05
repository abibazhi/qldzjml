import paddleocr
from PIL import Image, ImageDraw

# 初始化 PaddleOCR，仅启用文本检测，禁用文字识别
ocr = paddleocr.PaddleOCR(use_angle_cls=True, lang="ch", det=True, rec=False)

# 分析的图片路径
img_path = 'qldzjpng/001/167.png'

# 执行版面分析（仅检测文本块）
result = ocr.ocr(img_path, cls=True)

# 打印 result 的内容
print("检测结果如下：")
print(result)


# 打印文本块位置信息
for idx, line in enumerate(result):
    print(f"Text Block {idx + 1} Coordinates: ", line[0])  # 输出每个文本块的坐标

# 选：可视化输出，绘制文本框
image = Image.open(img_path).convert('RGB')
draw = ImageDraw.Draw(image)
for idx, line in enumerate(result):
    points = line[0][0]  # 提取文本块的四个角点坐标，这里只取坐标部分，忽略识别结果
    # 将坐标转换为整数类型
    int_points = [(int(coord[0]), int(coord[1])) for coord in points]
    flat_points = [coord for point in int_points for coord in point]

    # 确保坐标在图像范围内
    img_width, img_height = image.size
    for i in range(0, len(flat_points), 2):
        flat_points[i] = max(0, min(flat_points[i], img_width))
        flat_points[i + 1] = max(0, min(flat_points[i + 1], img_height))

    draw.polygon(flat_points, outline="red")
    text_x = max(flat_points[0], 0)
    text_y = max(flat_points[1], 0)
    draw.text((text_x, text_y), str(idx + 1), fill="red")  # 在每个文本块左上角标注序号

# 保存或显示带有文本框标记的图片
image.save("output_with_boxes.jpg")
image.show()
