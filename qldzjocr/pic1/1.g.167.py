import os
import numpy as np
from PIL import Image, ImageEnhance, ImageOps
from paddleocr import PaddleOCR
import traceback

# 初始化PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang="ch", det=True, rec=True)


def get_image_brightness(image):
    """
    计算图像的平均亮度。
    :param image: 输入的PIL图像对象。
    :return: 图像的平均亮度值。
    """
    # 将图像转换为灰度图像
    gray_image = image.convert('L')
    # 计算平均亮度
    mean_value = np.array(gray_image).mean()
    return mean_value


def preprocess_image(image):
    """
    对图像进行预处理，包括转换为灰度、增强对比度和二值化等。
    :param image: 输入的PIL图像对象。
    :return: 预处理后的图像。
    """
    # 转换为灰度图像
    gray_image = image.convert("L")
    
    # 增强对比度
    enhancer = ImageEnhance.Contrast(gray_image)
    enhanced_image = enhancer.enhance(2.0)  # 增强对比度
    
    # 二值化处理
    threshold = 150  # 根据实际情况调整此值
    binary_image = enhanced_image.point(lambda x: 255 if x > threshold else 0, '1')
    
    return binary_image.convert('RGB')  # 将二值图像转换回RGB格式以供OCR使用

def detect_text_in_image_part(image_path, part):
    """
    检测图片指定部分是否存在文本，并尝试识别文字。
    :param image_path: 图片路径。
    :param part: 图片的部分（左、右）。
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
            
            # 定义裁剪区域
            if part == 'left':
                box = (width*0//15, height*2//10, width*2//15, height*5//10)
            elif part == 'right':
                # 计算右侧对称的位置
                right_start_x = width - width*2//15  # 注意这里的2//15是为了与左侧保持一致
                right_end_x = width - width*0//15
                box = (right_start_x, height*2//10, right_end_x, height*5//10)
                #box = (width - width*2//14, height*0//10, width - width//14, height*5//10)
            else:
                raise ValueError("This version only supports processing the left or right part.")

            print(f"Cropping {part} part with box: {box}")  # 输出裁剪区域坐标

            cropped_img = img.crop(box)
            cropped_img.save(f"temp_{part}.png")  # 临时保存裁剪后的图片，方便检查

            # 获取裁剪部分的平均亮度
            brightness = get_image_brightness(cropped_img)
            print(f"{part.capitalize()} part brightness: {brightness}")
            
            # 根据亮度值判断是黑底白字还是白底黑字
            if brightness < 128:  # 假设阈值为128
                print(f"{part.capitalize()} part is dark background with light text.")
            else:
                print(f"{part.capitalize()} part is light background with dark text.")

            # 对裁剪后的图像进行预处理
            processed_img = preprocess_image(cropped_img)

            # 将裁剪并预处理后的PIL图像转换为numpy数组
            cropped_img_np = np.array(processed_img).astype(np.uint8)

            # 使用PaddleOCR进行文本检测
            result = ocr.ocr(cropped_img_np, cls=True)

            # 检查结果是否为None或空，并打印识别到的文字
            if result is None or len(result) < 1:
                has_text = False
                detected_texts = []
            else:
                has_text = True
                detected_texts = []
                for line in result:
                    if isinstance(line, list) and len(line) > 1 and isinstance(line[1], list) and len(line[1]) > 0:
                        text = line[1][0]
                        if isinstance(text, str):
                            detected_texts.append(text)
            
            if has_text:
                print(f"{part.capitalize()} part has text: {' '.join(detected_texts)}")
            else:
                print(f"{part.capitalize()} part does not have text.")
            return has_text
    except Exception as e:
        print(f"Error processing {image_path}'s {part} part:")
        traceback.print_exc()  # 打印详细的堆栈跟踪信息
        return False

if __name__ == "__main__":
    img_path = "qldzjpng/001/167.png"  # 确保此路径指向正确的图片

    # 测试仅对图片的左侧和右侧特定部分进行文本检测
    parts = ['left', 'right']
    for part in parts:
        detected_text = detect_text_in_image_part(img_path, part)
