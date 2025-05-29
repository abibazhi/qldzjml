"""
此脚本旨在遍历指定目录（qldzjpng）及其所有子目录中的图片文件，并对每张图片的左侧特定部分进行文本检测。
- 功能1：遍历整个qldzjpng目录及其子目录中的所有图片，按照目录的次序先后访问。
- 功能2：如果发现某个图片中，左侧有文字块识别出来，且该文字块是黑底白字（亮度条件），则记录其路径和文件名，并保存识别的文字到输出文件(output.txt)。
- 功能3：为了防止程序意外中止后可以继续，请记录识别的进度(progress.txt)，以便从中断的地方继续执行。
- 需求1：截取的图片不需要保存。
- 需求2：在控制台上输出处理进度，但不要输出调试信息。（调试时请保留详细的错误信息）
- 需求3：将上述功能和需求整理并放在代码前面作为说明。

使用方法：
确保设置了正确的根目录路径(root_directory)，然后运行脚本。
"""

import os
import numpy as np
from PIL import Image, ImageEnhance, ImageOps
from paddleocr import PaddleOCR
import traceback

# 初始化PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang="ch", det=True, rec=True)

def get_text_block_brightness(image, box):
    """
    计算指定区域内文字块的平均亮度。
    """
    cropped_img = image.crop(box)
    gray_image = cropped_img.convert('L')
    mean_value = np.array(gray_image).mean()
    return mean_value

def preprocess_image(image):
    """
    对图像进行预处理，包括转换为灰度、增强对比度和二值化等。
    """
    gray_image = image.convert("L")
    enhancer = ImageEnhance.Contrast(gray_image)
    enhanced_image = enhancer.enhance(2.0)
    threshold = 150
    binary_image = enhanced_image.point(lambda x: 255 if x > threshold else 0, '1')
    return binary_image.convert('RGB')

def detect_text_in_image_part(image_path, progress_file, output_file):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            
            # 定义左侧区域
            box_left = (width*0//15, height*2//10, width*2//15, height*5//10)
            
            cropped_img = img.crop(box_left)
            processed_img = preprocess_image(cropped_img)
            cropped_img_np = np.array(processed_img).astype(np.uint8)
            
            # 使用PaddleOCR进行文本检测
            result = ocr.ocr(cropped_img_np, cls=True)
            print(result)
            if (result != None) :
                print(result[0])
                if (result[0] != None) :
                    print(result[0][0])
            detected_texts = []
            for line in result:
                if isinstance(line, list) and len(line) > 1 and isinstance(line[1], list) and len(line[1]) > 0 and isinstance(line[1][0], str):
                    text = line[1][0]
                    print(text)
                    bbox = line[0]  # 文字块的边界框
                    brightness = get_text_block_brightness(img, bbox)
                    
                    #if brightness < 128:  # 如果文字块是黑底白字
                    detected_texts.append(text)
                    print(f"Detected dark background with light text block in file: {image_path}, Text: {text}, bright:{brightness}")
            
            if detected_texts:
                with open(output_file, 'a') as out_f:
                    out_f.write(f"Dark background with light text block in file: {image_path}\n")
                    for text in detected_texts:
                        out_f.write(f"Text: {text}\n")
            
            # 更新进度文件
            with open(progress_file, 'a') as pf:
                pf.write(f"{image_path}\n")
        
        print(f"Processed left part of {image_path}")
    except Exception as e:
        print(f"Error processing {image_path}'s left part.")
        traceback.print_exc()  # 输出详细的堆栈跟踪信息

def main(root_dir, progress_file='progress.txt', output_file='output.txt'):
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            processed_files = set(line.strip() for line in f.readlines())
    else:
        processed_files = set()

    total_files = sum(len(files) for _, _, files in os.walk(root_dir))
    processed_count = len(processed_files)

    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg')):
                full_path = os.path.join(subdir, file)
                if full_path in processed_files:
                    continue
                
                detect_text_in_image_part(full_path, progress_file, output_file)
                
                processed_count += 1
                print(f"Progress: {processed_count}/{total_files}")

if __name__ == "__main__":
    root_directory = "qldzjpng"
    main(root_directory)
