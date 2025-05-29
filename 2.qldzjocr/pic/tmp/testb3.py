import paddleocr
import numpy as np
from PIL import Image, ImageDraw

# 初始化 PaddleOCR，启用文字识别
ocr = paddleocr.PaddleOCR(use_angle_cls=True, lang="ch", det=True, rec=True, precision='fp16', det_limit_side_len=640)

# 要分析的图片路径
img_path = 'qldzjpng/001/165.png'

# 打开图片
image = Image.open(img_path).convert('RGB')
width, height = image.size

# 计算图片横向三等分的位置
one_third_width = width // 3
middle_left = one_third_width
middle_right = 2 * one_third_width

# 裁剪中间部分的图片
middle_image = image.crop((middle_left, 0, middle_right, height))

# 保存中间部分的图片（可选，用于调试）
middle_image.save("middle_image.jpg")

# 将 PIL 图像转换为 numpy 数组
middle_image_np = np.array(middle_image)

# 对中间部分的图片进行文字识别
middle_result = ocr.ocr(middle_image_np, cls=True)

# 打印中间部分的识别结果
print("中间部分的识别结果：")
if middle_result and middle_result[0]:
    for line in middle_result[0]:
        text = line[1][0]
        print(text)
else:
    print("未识别到文字。")

# 执行原有的版面分析（仅检测文本块）
result = ocr.ocr(img_path, cls=True)

draw = ImageDraw.Draw(image)

# 遍历每个检测到的文本块
for idx, line in enumerate(result[0]):
    # 提取文本块的坐标
    points = line[0]

    # 将坐标转换为整数类型
    int_points = [(int(point[0]), int(point[1])) for point in points]

    # 将坐标展平成一个简单的列表
    flat_points = [coord for point in int_points for coord in point]

    # 确保坐标在图像范围内
    img_width, img_height = image.size
    for i in range(0, len(flat_points), 2):
        flat_points[i] = max(0, min(flat_points[i], img_width))
        flat_points[i + 1] = max(0, min(flat_points[i + 1], img_height))

    # 绘制文本块的边框
    draw.polygon(flat_points, outline="red")

    # 确定文本标注的位置
    text_x = max(int_points[0][0], 0)
    text_y = max(int_points[0][1], 0)

    # 在文本块左上角标注序号
    draw.text((text_x, text_y), str(idx + 1), fill="red")

# 保存带有文本框标记的图片
image.save("output_with_boxes.jpg")

# 显示图片
image.show()
