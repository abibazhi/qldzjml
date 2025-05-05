import os
import cv2
from paddleocr import PaddleOCR

# 初始化PaddleOCR，指定语言为中文
ocr = PaddleOCR(use_angle_cls=True, lang="ch")

# 定义图片文件扩展名
image_extensions = ('.png', '.jpg', '.jpeg')

# 结果保存文件
output_file = 'recognition_results.txt'

def process_image(image_path):
    """处理单张图片并返回识别结果"""
    image = cv2.imread(image_path)

    # 进行文字识别
    result = ocr.ocr(image, cls=True)
    
    if len(result) > 0 and len(result[0]) > 0:
        # 获取第一个文本块
        first_text_block = result[0][0][1][0]
        return first_text_block
    else:
        return None

def write_result(f, relative_path, text):
    """将结果写入文件，并打印到控制台"""
    if text is not None:
        # 根据分隔符分割文本
        separators = ['丶', '、']
        current_text = ''
        for char in text:
            if char in separators:
                if current_text:
                    line = f"{relative_path}：{current_text}\n"
                    f.write(line)
                    print(line.strip())  # 打印到控制台
                    current_text = ''
            else:
                current_text += char
        if current_text:  # 写入最后一个文本片段
            line = f"{relative_path}：{current_text}\n"
            f.write(line)
            print(line.strip())  # 打印到控制台
    else:
        line = f"{relative_path}：未检测到符合条件的文本块\n"
        f.write(line)
        print(line.strip())  # 打印到控制台

# 打开文件以写入模式
with open(output_file, 'w', encoding='utf-8') as f:
    # 遍历目录及其子目录
    root_dir = 'qldzjpng_filtered'
    total_images = sum([len(files) for root, dirs, files in os.walk(root_dir) if any(file.lower().endswith(image_extensions) for file in files)])
    processed_images = 0
    for root, dirs, files in os.walk(root_dir):
        # 对目录名和文件名进行排序
        dirs.sort()
        files.sort()
        for file in files:
            if file.lower().endswith(image_extensions):
                image_path = os.path.join(root, file)
                relative_path = os.path.relpath(image_path, root_dir)

                # 处理图像并获取识别结果
                recognized_text = process_image(image_path)
                
                # 打印图片路径和识别文本
                print(f"Processing {relative_path}:")
                if recognized_text:
                    print(f"Recognized Text: {recognized_text}")
                else:
                    print("No text recognized.")

                # 将结果写入文件
                write_result(f, relative_path, recognized_text)

                processed_images += 1
                print(f"已处理 {processed_images}/{total_images} 图像: {relative_path}")

print(f"所有图像处理完成，识别结果已保存到 {output_file}")
