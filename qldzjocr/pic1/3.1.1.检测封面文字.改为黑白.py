import os
from PIL import Image
import numpy as np
from paddleocr import PaddleOCR

# 初始化PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang="ch", det=True, rec=True)

def ensure_three_channels(image):
    """确保图像有三个通道"""
    if image.mode == 'RGB':
        return image
    elif image.mode in ['1', 'L']:  # 如果图像是黑白或灰度图像
        return image.convert('RGB')
    else:
        raise ValueError(f"不支持的图像模式: {image.mode}")

def process_image(img_path, output_file):
    try:
        with Image.open(img_path) as image:
            image = ensure_three_channels(image)
            width, height = image.size
            
            # 检查图像尺寸是否足够大以进行裁剪
            if width < 1480 or height < 2660:
                print(f"跳过 {img_path}：图像尺寸不足")
                return
            
            # 裁剪指定区域
            box = (1015, 720, 1480, 2660)
            cropped_image = image.crop(box)

            # 将PIL图像转换为numpy数组
            cropped_image_np = np.asarray(cropped_image)

            # OCR识别
            result = ocr.ocr(cropped_image_np, cls=True)

            text_block_count = len(result[0]) if result and result[0] else 0  # 统计识别到的文本块总数
            detected_texts = [line[1][0] for line in result[0]] if result and result[0] else []

            if text_block_count > 0:
                first_text = detected_texts[0]
                all_texts = ', '.join(detected_texts)
                with open(output_file, 'a') as file:
                    file.write(f"图片路径: {img_path}, 第一个文本块中的文字: {first_text}, 所有文本块中的文字: {all_texts}\n")
                print(f"已处理 {img_path}")

    except IOError as e:
        print(f"无法打开或读取图片 {img_path}: {str(e)}")
    except Exception as e:
        print(f"处理 {img_path} 时出现错误: {str(e)}")

def main(root_dir, output_file):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg')):
                img_path = os.path.join(subdir, file)
                process_image(img_path, output_file)

if __name__ == "__main__":
    root_directory = "./selected_images/"  # 修改为你需要遍历的目录
    output_file = "detected_texts_output1.txt"  # 输出文件名
    main(root_directory, output_file)
