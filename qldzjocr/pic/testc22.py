import os
import cv2
import numpy as np
from paddleocr import PaddleOCR
from xpinyin import Pinyin  # 用于简体字转换，需要先安装：pip install xpinyin
import re

# 初始化PaddleOCR，指定语言为中文
ocr = PaddleOCR(use_angle_cls=True, lang="ch")

# 定义图片文件扩展名
image_extensions = ('.png', '.jpg', '.jpeg')

# 结果保存文件
output_file = 'recognition_results.txt'
comparison_file = 'comparison_results.html'

# 读取文本文件内容
with open('../qldzj-ml/3.sutra-name-list.txt', 'r', encoding='utf-8') as file:
    target_lines = file.read().splitlines()

# 打开文件以写入模式
with open(output_file, 'w', encoding='utf-8') as f:
    # 遍历目录及其子目录
    root_dir = 'qldzjpng_filtered'
    total_images = sum([len(files) for root, dirs, files in os.walk(root_dir) if any(file.lower().endswith(image_extensions) for file in files)])
    processed_images = 0
    html_table = "<table border='1'><tr><th>相对目录</th><th>目标文本</th><th>识别文本（简体）</th><th>差异</th></tr>"
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

                relative_path = os.path.relpath(image_path, root_dir)
                target_text = target_lines[processed_images] if processed_images < len(target_lines) else ""

                if len(result) > 0 and len(result[0]) > 1:
                    # 获取第二个文本块的识别文字
                    second_text_block_text = result[0][1][1][0]
                    # 转换为简体字
                    p = Pinyin()
                    simplified_text = p.get_pinyin(second_text_block_text, tone_marks='marks')
                    simplified_text = re.sub('[^\u4e00-\u9fa5a-zA-Z0-9]', '', simplified_text)
                    # 比较差异
                    diff = ""
                    for t, r in zip(target_text, simplified_text):
                        if t != r:
                            diff += f"目标：{t}，识别：{r}；"
                    line = f"{relative_path}：{second_text_block_text}\n"
                    f.write(line)
                    html_table += f"<tr><td>{relative_path}</td><td>{target_text}</td><td>{simplified_text}</td><td>{diff}</td></tr>"
                    print(f"已处理 {processed_images + 1}/{total_images}：{relative_path}，识别文字：{second_text_block_text}")
                else:
                    line = f"{relative_path}：未检测到第二个文本块\n"
                    f.write(line)
                    html_table += f"<tr><td>{relative_path}</td><td>{target_text}</td><td>未检测到第二个文本块</td><td>未检测到第二个文本块</td></tr>"
                    print(f"已处理 {processed_images + 1}/{total_images}：{relative_path}，未检测到第二个文本块")

                processed_images += 1

    html_table += "</table>"
    with open(comparison_file, 'w', encoding='utf-8') as html_f:
        html_f.write(html_table)

print(f"识别结果已保存到 {output_file}")
print(f"比较结果已保存到 {comparison_file}")
