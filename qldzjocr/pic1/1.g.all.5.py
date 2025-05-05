"""
此脚本旨在遍历指定目录（qldzjpng）及其所有子目录中的图片文件，并对每张图片的左侧特定部分进行文本检测。
- 功能1：遍历整个qldzjpng目录及其子目录中的所有图片，按照目录的次序先后访问。
- 功能2：如果发现某个图片中，左侧有文字块识别出来，则记录：
    1. 文字块中的文字；
    2. 把这个文字块所在的图片另外截图并保存，文件名可以根据原始图片名取，并放入统一的临时目录中；
    3. 这个文字块对应图片的亮度。
    输出的信息将包括原始图片路径、检测到的文字、文字所在临时图片的路径，该临时图片的亮度。
- 功能3：为了防止程序意外中止后可以继续，请记录识别的进度(progress.txt)，以便从中断的地方继续执行。
- 需求1：截取的图片不需要保存（对于非调试模式）。
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

def save_text_block_image(image, box, output_dir, original_filename):
    """
    根据给定的边界框从图像中裁剪出文字块并保存。
    """
    cropped_img = image.crop(box)
    temp_image_name = f"{os.path.splitext(original_filename)[0]}_textblock_{box}.png"
    temp_image_path = os.path.join(output_dir, temp_image_name)
    cropped_img.save(temp_image_path)
    return temp_image_path

def detect_text_in_image_part(image_path, progress_file, output_file, temp_dir):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            
            # 定义左侧区域
            box_left = (width*0//15, height*2//10, width*2//15, height*5//10)
            
            cropped_img = img.crop(box_left)
            processed_img = cropped_img.convert("L")  # 转为灰度图以计算亮度
            cropped_img_np = np.array(cropped_img).astype(np.uint8)
            
            # 使用PaddleOCR进行文本检测
            result = ocr.ocr(cropped_img_np, cls=True)
            
            detected_texts = []
            for line in result:
                if isinstance(line, list) and len(line) > 1 and isinstance(line[1], list) and len(line[1]) > 0 and isinstance(line[1][0], str):
                    text = line[1][0]
                    bbox = [int(coord) for point in line[0] for coord in point]  # 文字块的边界框
                    
                    # 调整bbox坐标相对于裁剪区域的位置
                    adjusted_bbox = (bbox[0], bbox[1], bbox[4], bbox[5])
                    
                    brightness = get_text_block_brightness(img, adjusted_bbox)
                    
                    # 保存文字块图片
                    temp_image_path = save_text_block_image(img, adjusted_bbox, temp_dir, os.path.basename(image_path))
                    
                    detected_texts.append((text, brightness, temp_image_path))
                    print(f"Detected text block in file: {image_path}, Text: {text}, Brightness: {brightness}")
            
            if detected_texts:
                with open(output_file, 'a') as out_f:
                    for text, brightness, temp_image_path in detected_texts:
                        out_f.write(f"Original Image Path: {image_path}\n")
                        out_f.write(f"Detected Text: {text}\n")
                        out_f.write(f"Text Block Image Path: {temp_image_path}\n")
                        out_f.write(f"Brightness of Text Block Image: {brightness}\n\n")
            
            # 更新进度文件
            with open(progress_file, 'a') as pf:
                pf.write(f"{image_path}\n")
        
        print(f"Processed left part of {image_path}")
    except Exception as e:
        print(f"Error processing {image_path}'s left part.")
        traceback.print_exc()  # 输出详细的堆栈跟踪信息

def main(root_dir, progress_file='progress.txt', output_file='output.txt', temp_dir='temp_images'):
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
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
                
                detect_text_in_image_part(full_path, progress_file, output_file, temp_dir)
                
                processed_count += 1
                print(f"Progress: {processed_count}/{total_files}")

if __name__ == "__main__":
    root_directory = "qldzjpng"
    main(root_directory)
