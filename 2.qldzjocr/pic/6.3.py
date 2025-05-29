import os
import cv2
from paddleocr import PaddleOCR

# 初始化PaddleOCR，指定语言为中文
ocr = PaddleOCR(use_angle_cls=True, lang="ch")

# 定义图片文件扩展名
image_extensions = ('.png', '.jpg', '.jpeg')

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

def write_result(relative_path, text):
    """将结果逐行打印在控制台上"""
    if text is not None:
        # 根据分隔符分割文本
        separators = ['丶', '、']
        current_text = ''
        for char in text:
            if char in separators:
                if current_text:
                    print(f"{relative_path}：{current_text}")
                    current_text = ''
            else:
                current_text += char
        if current_text:  # 打印最后一个文本片段
            print(f"{relative_path}：{current_text}")
    else:
        print(f"{relative_path}：未检测到符合条件的文本块")

# 遍历目录及其子目录
root_dir = 'qldzjpng_filtered'
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
            
            # 输出结果到控制台
            write_result(relative_path, recognized_text)

print("所有图像处理完成")
