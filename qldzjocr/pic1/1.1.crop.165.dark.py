import paddleocr
from PIL import Image, ImageDraw, ImageStat

# 初始化 PaddleOCR，启用文本检测和文字识别
ocr = paddleocr.PaddleOCR(use_angle_cls=True, lang="ch", det=True, rec=True, precision='fp16', det_limit_side_len=640)

# 要分析的图片路径
# img_path = 'qldzjpng/001/166.png'
img_path = 'qldzjpng/001/165.png'

def detect_text_background(cropped_image):
    """ 分析给定图像区域的颜色分布，返回背景类型 """
    # 转换为灰度图像
    gray_image = cropped_image.convert('L')

    # 使用ImageStat统计灰度图像的统计数据
    stat = ImageStat.Stat(gray_image)
    mean_value = stat.mean[0]  # 获取平均亮度

    # 判断背景颜色
    if mean_value < 128:  # 阈值可以根据实际情况调整
        return "Dark background with light text"
    else:
        return "Light background with dark text"

try:
    # 打开并裁剪图片
    image = Image.open(img_path).convert('RGB')
    width, height = image.size  # 获取原图尺寸
    box = (200, 0, 530, 3508)  # 设定裁剪区域，格式为(left, upper, right, lower)
    cropped_image = image.crop(box)  # 裁剪图像

    # 保存裁剪后的图片
    cropped_image_path = "cropped_165.png"
    cropped_image.save(cropped_image_path)

    # 对裁剪后的图像执行版面分析（检测和识别文本）
    result = ocr.ocr(cropped_image_path, cls=True)

    # 创建绘图对象
    draw = ImageDraw.Draw(cropped_image)

    for idx, line in enumerate(result[0]):  # 注意：PaddleOCR 的结果是嵌套列表，需要取 result[0]
        # 提取文本块的坐标和识别出的文字
        points = line[0]
        recognized_text = line[1][0]  # 识别出的文字

        # 提取文本块
        # 由于坐标是基于裁剪后的图像，需要将其转换为原始图像的坐标
        adjusted_points = [(point[0] + box[0], point[1] + box[1]) for point in points]
        x_coords = [point[0] for point in adjusted_points]
        y_coords = [point[1] for point in adjusted_points]
        cropped_text_block = image.crop((min(x_coords), min(y_coords), max(x_coords), max(y_coords)))

        # 计算文本块的颜色分布
        background_type = detect_text_background(cropped_text_block)
        print(f"文本 {idx + 1}: {recognized_text} 的背景类型: {background_type}")

        # 将坐标转换为整数类型
        int_points = [(int(point[0]), int(point[1])) for point in points]
        flat_points = [coord for point in int_points for coord in point]

        # 绘制文本块的边框
        draw.polygon(flat_points, outline="red")

        # 确定文本标注的位置
        text_x = max(int_points[0][0], 0)
        text_y = max(int_points[0][1], 0)

        # 在文本块左上角标注序号和背景类型信息
        draw.text((text_x, text_y), f"{idx + 1}: {background_type}", fill="red")

    # 保存带有文本框标记和背景信息的图片
    cropped_image.save("output_cropped_165_with_boxes.jpg")

    # 显示图片
    cropped_image.show()

except Exception as e:
    print(f"出现错误: {e}")
