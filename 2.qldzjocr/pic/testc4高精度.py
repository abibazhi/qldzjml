import paddleocr
import numpy as np
from PIL import Image, ImageEnhance
from opencc import OpenCC
import os
import re

# 初始化 PaddleOCR 和简繁转换器
ocr = paddleocr.PaddleOCR(
    use_angle_cls=True,
    lang="ch",
    det=True,
    rec=True,
    precision='fp16',
    det_limit_side_len=960,
    rec_image_shape="3, 64, 320",
    det_db_thresh=0.3,
    det_db_box_thresh=0.5,
    det_db_unclip_ratio=1.6,
)

cc = OpenCC('t2s')

# 图片目录和文本文件路径
img_base_dir = 'qldzjpng_filtered/'
text_file_path = 'sutra.list.txt'

# 读取文本文件内容到列表中
with open(text_file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 去除每行的换行符
lines = [line.strip() for line in lines]

def natural_sort_key(s):
    """用于自然排序的关键字函数"""
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def preprocess_image(image):
    """图像预处理函数"""
    # 灰度化
    image = image.convert('L')
    
    # 增强对比度
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)
    
    return image

def process_image(img_path):
    """处理单张图片"""
    # 打开并预处理图片
    image = Image.open(img_path).convert('RGB')
    image = preprocess_image(image)
    width, height = image.size

    # 计算图片横向三等分的位置并裁剪中间部分
    one_third_width = width // 3
    middle_image = image.crop((one_third_width, 0, 2 * one_third_width, height))

    # 将 PIL 图像转换为 numpy 数组
    middle_image_np = np.array(middle_image)

    # 对中间部分的图片进行文字识别
    middle_result = ocr.ocr(middle_image_np, cls=True)

    # 如果有识别结果，仅取第一个文字块
    if middle_result and middle_result[0]:
        first_line = middle_result[0][0]  # 获取第一个文字块
        text = first_line[1][0]  # 提取文字内容
        simplified_text = cc.convert(text)  # 简繁转换

        print(f"图片 {img_path} 中识别到的文字: {simplified_text}")

        # 检查该文字是否在文本文件中
        if simplified_text in lines:
            line_number = lines.index(simplified_text) + 1  # 行号从1开始计数
            print(f"在文本文件中的行号为: {line_number}")
        else:
            print("未找到匹配的文字")
    else:
        print(f"图片 {img_path} 中未识别到任何文字")

# 获取所有子目录并按数字顺序排序
subdirs = sorted([name for name in os.listdir(img_base_dir) if os.path.isdir(os.path.join(img_base_dir, name))], key=natural_sort_key)

for subdir in subdirs:
    subdir_path = os.path.join(img_base_dir, subdir)
    
    # 获取当前子目录下的所有图片文件并按数字顺序排序
    files = sorted([f for f in os.listdir(subdir_path) if f.endswith('.png')], key=natural_sort_key)
    
    for file in files:
        img_path = os.path.join(subdir_path, file)
        process_image(img_path)
