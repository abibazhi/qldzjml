import os
import paddleocr
from PIL import Image, ImageDraw, ImageStat

# 初始化 PaddleOCR，启用文本检测和文字识别
ocr = paddleocr.PaddleOCR(use_angle_cls=True, lang="ch", det=True, rec=True, precision='fp16', det_limit_side_len=640)

# 要分析的图片目录
img_dir = 'qldzjpng'

# 记录进度的文件
progress_file = 'progress.txt'

# 记录结果的文件
result_file = 'black_background_results.txt'

def detect_text_background(cropped_image):
    """ 分析给定图像区域的颜色分布，返回背景类型 """
    # 转换为灰度图像
    gray_image = cropped_image.convert('L')

    # 使用 ImageStat 统计灰度图像的统计数据
    stat = ImageStat.Stat(gray_image)
    mean_value = stat.mean[0]  # 获取平均亮度

    # 判断背景颜色
    if mean_value < 128:  # 阈值可以根据实际情况调整
        return "Dark background with light text"
    else:
        return "Light background with dark text"

# 读取已处理的图片列表
if os.path.exists(progress_file):
    with open(progress_file, 'r') as f:
        processed_images = set(f.read().splitlines())
else:
    processed_images = set()

# 遍历目录下的所有图片文件
for root, dirs, files in os.walk(img_dir):
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(root, file)
            if img_path in processed_images:
                continue

            try:
                # 打开图片
                image = Image.open(img_path).convert('RGB')

                # 对图像执行版面分析（检测和识别文本）
                result = ocr.ocr(img_path, cls=True)

                has_dark_background = False
                for line in result[0]:
                    # 提取文本块的坐标
                    points = line[0]
                    x_coords = [point[0] for point in points]
                    y_coords = [point[1] for point in points]
                    cropped_text_block = image.crop((min(x_coords), min(y_coords), max(x_coords), max(y_coords)))

                    # 计算文本块的颜色分布
                    background_type = detect_text_background(cropped_text_block)
                    if background_type == "Dark background with light text":
                        has_dark_background = True
                        break

                if has_dark_background:
                    with open(result_file, 'a') as f:
                        f.write(f'{img_path}\n')

                # 记录已处理的图片
                with open(progress_file, 'a') as f:
                    f.write(f'{img_path}\n')
                processed_images.add(img_path)

                print(f'Processed: {img_path}')

            except Exception as e:
                print(f"Error processing {img_path}: {e}")

print("Processing completed.")
