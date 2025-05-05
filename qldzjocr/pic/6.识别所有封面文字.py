import os
import cv2
import numpy as np
from paddleocr import PaddleOCR

# 初始化PaddleOCR，指定语言为中文
ocr = PaddleOCR(use_angle_cls=True, lang="ch")

# 定义图片文件扩展名
image_extensions = ('.png', '.jpg', '.jpeg')

# 结果保存文件
output_file = 'recognition_results.txt'

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
                image = cv2.imread(image_path)

                # 进行文字识别
                result = ocr.ocr(image, cls=True)

                if len(result) > 0 and len(result[0]) > 1:
                    # 获取第二个文本块的识别文字
                    second_text_block_text = result[0][1][1][0]
                    relative_path = os.path.relpath(image_path, root_dir)
                    line = f"{relative_path}：{second_text_block_text}\n"
                    f.write(line)
                    print(f"已处理 {processed_images + 1}/{total_images}：{relative_path}，识别文字：{second_text_block_text}")
                else:
                    relative_path = os.path.relpath(image_path, root_dir)
                    line = f"{relative_path}：未检测到第二个文本块\n"
                    f.write(line)
                    print(f"已处理 {processed_images + 1}/{total_images}：{relative_path}，未检测到第二个文本块")

                processed_images += 1

print(f"识别结果已保存到 {output_file}")
