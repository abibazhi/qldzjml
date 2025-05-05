import os
import numpy as np
from PIL import Image
from paddleocr import PaddleOCR
import shutil
import traceback

# 初始化PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang="ch", det=True, rec=True, precision='fp16', det_limit_side_len=640)

def write_to_file(file_path, img_path, text_block_count_primary, detected_texts_primary, secondary_text_block_count=None, secondary_detected_texts=None):
    """将信息写入文件"""
    with open(file_path, 'a') as file:  # 使用'a'模式以追加方式打开文件
        primary_info = f"图片路径: {img_path}, 主区域检测到的文本块总数: {text_block_count_primary}, 文本内容: {', '.join(detected_texts_primary)}"
        if secondary_text_block_count and secondary_detected_texts:
            secondary_info = f", 辅助区域检测到的文本块总数: {secondary_text_block_count}, 文本内容: {', '.join(secondary_detected_texts)}"
        else:
            secondary_info = ""
        file.write(f"{primary_info}{secondary_info}\n")

def move_image_to_detected(img_path, detected_dir):
    """将图片移动到检测到的目录"""
    os.makedirs(detected_dir, exist_ok=True)  # 确保目标目录存在
    filename = os.path.basename(img_path)
    dest_path = os.path.join(detected_dir, filename)
    shutil.move(img_path, dest_path)
    print(f"已将图片 {img_path} 移动到 {dest_path}")

def process_image(img_path, output_file, detected_dir):
    try:
        print(f"正在处理图片: {img_path}")
        # 尝试打开图片
        with Image.open(img_path) as image:
            # 确保图像为RGB模式
            image = image.convert('RGB')
            width, height = image.size

            # 检查图像尺寸是否足够大以进行裁剪
            if width < 2240 or height < 1700:
                print(f"跳过 {img_path}：图像尺寸不足")
                return

            # 主区域裁剪
            box_primary = (width - 530, 250, 2240, 1700)
            cropped_image_primary = image.crop(box_primary)

            # 将PIL图像转换为numpy数组
            cropped_image_np_primary = np.asarray(cropped_image_primary)

            # 主区域OCR识别
            result_primary = ocr.ocr(cropped_image_np_primary, cls=True)

            text_block_count_primary = len(result_primary[0]) if result_primary and result_primary[0] else 0  # 统计识别到的文本块总数
            detected_texts_primary = [line[1][0] for line in result_primary[0]] if result_primary and result_primary[0] else []

            if text_block_count_primary > 0:
                # 如果主区域检测到文本块，则记录并移动图片
                print(f"图片路径: {img_path}, 主区域检测到的文本块总数: {text_block_count_primary}, 文本内容: {detected_texts_primary}")
                write_to_file(output_file, img_path, text_block_count_primary, detected_texts_primary)
                move_image_to_detected(img_path, detected_dir)
            else:
                # 如果主区域没有检测到文本块，则检查辅助区域
                box_secondary = (850, 1450, 1650, 1550)
                cropped_image_secondary = image.crop(box_secondary)

                # 将PIL图像转换为numpy数组
                cropped_image_np_secondary = np.asarray(cropped_image_secondary)

                # 辅助区域OCR识别
                result_secondary = ocr.ocr(cropped_image_np_secondary, cls=True)

                text_block_count_secondary = len(result_secondary[0]) if result_secondary and result_secondary[0] else 0  # 统计识别到的文本块总数
                detected_texts_secondary = [line[1][0] for line in result_secondary[0]] if result_secondary and result_secondary[0] else []

                # 检查辅助区域是否包含特定字符串
                if any("清刻龍藏" in text for text in detected_texts_secondary):
                    print(f"图片路径: {img_path}, 辅助区域检测到的文本块总数: {text_block_count_secondary}, 文本内容: {detected_texts_secondary}")
                    write_to_file(output_file, img_path, text_block_count_primary, detected_texts_primary, text_block_count_secondary, detected_texts_secondary)
                    move_image_to_detected(img_path, detected_dir)

    except IOError as e:
        print(f"无法打开或读取图片 {img_path}: {str(e)}\n{traceback.format_exc()}")
    except Exception as e:
        # 打印详细的异常信息
        print(f"处理 {img_path} 时出现错误: {str(e)}\n{traceback.format_exc()}")

def main(root_dir, output_file, detected_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg')):
                img_path = os.path.join(subdir, file)
                process_image(img_path, output_file, detected_dir)

if __name__ == "__main__":
    root_directory = "selected_images"  # 修改为你需要遍历的目录
    output_file = "detected_texts_output.txt"  # 输出文件名
    detected_directory = os.path.join(root_directory, "detected_images")  # 检测到的图片存放目录
    main(root_directory, output_file, detected_directory)
