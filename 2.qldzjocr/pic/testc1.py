import paddleocr
import numpy as np
from PIL import Image
from opencc import OpenCC
import os

# 初始化 PaddleOCR 和简繁转换器
ocr = paddleocr.PaddleOCR(use_angle_cls=True, lang="ch", det=True, rec=True, precision='fp16', det_limit_side_len=640)
cc = OpenCC('t2s')

# 图片目录和文本文件路径
img_dir = 'qldzjpng/001/'
text_file_path = 'sutra.list.txt'

# 读取文本文件内容到列表中
with open(text_file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 去除每行的换行符
lines = [line.strip() for line in lines]

# 遍历图片目录中的所有图片文件
for img_name in os.listdir(img_dir):
    if img_name.endswith('.png'):  # 只处理PNG图片
        img_path = os.path.join(img_dir, img_name)

        # 打开图片
        image = Image.open(img_path).convert('RGB')
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

            # 检查该文字是否在文本文件中
            if simplified_text in lines:
                line_number = lines.index(simplified_text) + 1  # 行号从1开始计数
                print(f"图片 {img_name} 中找到匹配的文字: {simplified_text}, 在文本文件中的行号为: {line_number}")
