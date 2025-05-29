import os
import numpy as np
from PIL import Image
from paddleocr import PaddleOCR
import traceback

# 初始化PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang="ch", det=True, rec=True, precision='fp16', det_limit_side_len=640)

def write_to_file(file_path, img_path, text_block_count, detected_texts):
    """将信息写入文件"""
    with open(file_path, 'a') as file:  # 使用'a'模式以追加方式打开文件
        file.write(f"图片路径: {img_path}, 检测到的文本块总数: {text_block_count}, 文本内容: {', '.join(detected_texts)}\n")

def process_image(img_path, output_file):
    try:
        print(f"正在处理图片: {img_path}")
        # 尝试打开图片
        with Image.open(img_path) as image:
            # 确保图像为RGB模式
            image = image.convert('RGB')
            width, height = image.size
            
            # 检查图像尺寸是否足够大以进行裁剪
            if width < 530 or height < 1700:
                print(f"跳过 {img_path}：图像尺寸不足")
                return
            
            # 对称的裁剪区域
            box = (width - 530, 0, width, 1700)
            cropped_image = image.crop(box)

            # 将PIL图像转换为numpy数组
            cropped_image_np = np.asarray(cropped_image)

            # OCR识别
            result = ocr.ocr(cropped_image_np, cls=True)

            text_block_count = len(result[0]) if result and result[0] else 0  # 统计识别到的文本块总数
            detected_texts = [line[1][0] for line in result[0]] if result and result[0] else []

            if text_block_count > 0:
                print(f"图片路径: {img_path}, 检测到的文本块总数: {text_block_count}, 文本内容: {detected_texts}")
                # 将结果写入文件
                write_to_file(output_file, img_path, text_block_count, detected_texts)

    except IOError as e:
        print(f"无法打开或读取图片 {img_path}: {str(e)}\n{traceback.format_exc()}")
    except Exception as e:
        # 打印详细的异常信息
        print(f"处理 {img_path} 时出现错误: {str(e)}\n{traceback.format_exc()}")

def main(root_dir, output_file):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg')):
                img_path = os.path.join(subdir, file)
                process_image(img_path, output_file)

if __name__ == "__main__":
    root_directory = "selected_images"  # 修改为你需要遍历的目录
    output_file = "detected_texts_output.txt"  # 输出文件名
    main(root_directory, output_file)
