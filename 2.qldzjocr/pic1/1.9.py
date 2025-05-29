import os
import numpy as np
from PIL import Image
from paddleocr import PaddleOCR
import traceback

# 初始化PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang="ch", det=True, rec=True)

def detect_text_in_image_part(image_path, part):
    """
    检测图片指定部分是否存在文本。
    :param image_path: 图片路径。
    :param part: 图片的部分（左、中、右）。
    """
    try:
        # 检查图片文件是否存在
        if not os.path.exists(image_path):
            print(f"Image file {image_path} does not exist.")
            return False

        # 打开图片并获取尺寸
        with Image.open(image_path) as img:
            width, height = img.size
            print(f"Image size: {width}x{height}")  # 输出图片尺寸

            if part == 'left':
                box = (0, 0, width//3, height)
            elif part == 'middle':
                box = (width//3, 0, 2*width//3, height)
            else:  # right
                box = (2*width//3, 0, width, height)

            print(f"Cropping {part} part with box: {box}")  # 输出裁剪区域坐标

            cropped_img = img.crop(box)
            cropped_img.save(f"temp_{part}.png")  # 临时保存裁剪后的图片，方便检查

            # 将裁剪后的PIL图像转换为numpy数组
            cropped_img_np = np.array(cropped_img).astype(np.uint8)

            # 使用PaddleOCR进行文本检测
            result = ocr.ocr(cropped_img_np, cls=True)

            # 根据检测结果判断是否有文本
            has_text = len(result[0]) > 0  # 如果检测到了文本
            print(f"{part.capitalize()} part {'has' if has_text else 'does not have'} text.")
            return has_text
    except Exception as e:
        print(f"Error processing {image_path}'s {part} part:")
        traceback.print_exc()  # 打印详细的堆栈跟踪信息
        return False

if __name__ == "__main__":
    img_path = "qldzjpng/001/165.png"  # 确保此路径指向正确的图片

    # 测试仅对图片的左部分进行文本检测
    left_has_text = detect_text_in_image_part(img_path, 'left')
