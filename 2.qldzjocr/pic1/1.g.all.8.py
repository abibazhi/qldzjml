import os
import numpy as np
from PIL import Image
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

def save_text_block_image(image, box, output_dir, original_filepath, index):
    """
    根据给定的边界框从图像中裁剪出文字块并保存。
    """
    cropped_img = image.crop(box)
    original_filename = os.path.basename(original_filepath)
    directory_name = os.path.dirname(original_filepath).split('/')[-1]  # 获取最后一个目录名
    temp_image_name = f"{directory_name}-{original_filename.split('.')[0]}-{index}.png"
    temp_image_path = os.path.join(output_dir, temp_image_name)
    cropped_img.save(temp_image_path)
    return temp_image_path

def detect_text_in_image_part(image_path, progress_file, output_file, low_brightness_output_file, temp_dir):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            
            # 定义左侧区域
            box_left = (width*0//15, height*2//10, width*2//15, height*5//10)
            
            cropped_img = img.crop(box_left)
            cropped_img_np = np.array(cropped_img).astype(np.uint8)
            
            # 使用PaddleOCR进行文本检测
            result = ocr.ocr(cropped_img_np, cls=True)
            print(f"Raw result: {result}")  # 打印原始结果
            
            detected_texts = []
            if isinstance(result, list):
                for idx, first_level in enumerate(result):
                    print(f"Parsing first level: {first_level}")  # 打印第一层
                    
                    if isinstance(first_level, list) and len(first_level) > 0:
                        for second_level in first_level:
                            print(f"Parsing second level: {second_level}")  # 打印第二层
                            
                            if isinstance(second_level, list) and len(second_level) == 2 and all(isinstance(point, list) and len(point) == 2 for point in second_level[0]):
                                bbox = [coord for point in second_level[0] for coord in point]  # 文字块的边界框
                                print(f"BBox coordinates: {bbox}")  # 打印边界框坐标
                                
                                text_info = second_level[1]
                                if isinstance(text_info, tuple) and len(text_info) == 2 and isinstance(text_info[0], str) and isinstance(text_info[1], float):
                                    text = text_info[0]
                                    confidence = text_info[1]
                                    print(f"Text: {text}, Confidence: {confidence}")  # 打印识别的文字及其置信度
                                    
                                    adjusted_bbox = (min(bbox[::2]), min(bbox[1::2]), max(bbox[::2]), max(bbox[1::2]))
                                    brightness = get_text_block_brightness(img, adjusted_bbox)
                                    print(f"Brightness of the text block: {brightness}")  # 打印亮度值
                                    
                                    # 保存文字块图片
                                    temp_image_path = save_text_block_image(img, adjusted_bbox, temp_dir, image_path, idx)
                                    print(f"Saved text block image to: {temp_image_path}")  # 打印临时图片路径
                                    
                                    detected_texts.append((text, brightness, temp_image_path))
                                    
                                    # 检查亮度是否小于200，并将其记录在单独的文件中
                                    if brightness < 200:
                                        with open(low_brightness_output_file, 'a') as lb_out_f:
                                            lb_out_f.write(f"Original Image Path: {image_path}\n")
                                            lb_out_f.write(f"Detected Text: {text}\n")
                                            lb_out_f.write(f"Text Block Image Path: {temp_image_path}\n")
                                            lb_out_f.write(f"Brightness of Text Block Image: {brightness}\n\n")
                                else:
                                    print("Unexpected format for text information.")
                            else:
                                print("Unexpected format for second level item.")
                    else:
                        print("Unexpected format for first level item.")
            else:
                print("Result is not a list.")
            
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

def main(root_dir, progress_file='progress.txt', output_file='output.txt', low_brightness_output_file='low_brightness_output.txt', temp_dir='temp_images'):
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
                
                detect_text_in_image_part(full_path, progress_file, output_file, low_brightness_output_file, temp_dir)
                
                processed_count += 1
                print(f"Progress: {processed_count}/{total_files}")

if __name__ == "__main__":
    root_directory = "qldzjpng"
    main(root_directory)
