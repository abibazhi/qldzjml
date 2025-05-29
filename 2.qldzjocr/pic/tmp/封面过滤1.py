import os
import paddleocr
import logging
import json

# 设置日志级别为 ERROR，抑制调试信息输出
logging.getLogger('ppocr').setLevel(logging.ERROR)

# 初始化 PaddleOCR，仅启用文本检测，禁用文字识别
ocr = paddleocr.PaddleOCR(use_angle_cls=True, lang="ch", det=True, rec=False, det_limit_side_len=640, ir_optim=False, use_tensorrt=False)

# 要分析的根图片目录路径
image_dir = 'qldzjpng'

# 用于存储所有图片信息的字典
all_info = {}

# 递归遍历目录及其子目录
for root, dirs, files in os.walk(image_dir):
    # 获取当前目录相对于根目录的相对路径作为目录名
    relative_dir = os.path.relpath(root, image_dir)
    if relative_dir == '.':
        relative_dir = ''
    # 存储当前目录下的图片信息
    dir_info = {}
    for filename in files:
        if filename.endswith('.png'):
            img_path = os.path.join(root, filename)
            # 执行版面分析（仅检测文本块）
            result = ocr.ocr(img_path, cls=True)
            # 计算文本块总数
            text_block_count = len(result[0])
            # 仅当文本块数目小于 10 时记录信息并输出到控制台
            if text_block_count < 10:
                # 记录文件名及其对应的文本块数量
                dir_info[filename] = text_block_count
                # 输出当前图片的处理结果到控制台
                print(f"目录名: {relative_dir}, 文件名: {filename}, 文件块数: {text_block_count}")
    if dir_info:
        all_info[relative_dir] = dir_info

# 将所有信息保存为 JSON 格式
output_json = json.dumps(all_info, indent=4, ensure_ascii=False)

# 将 JSON 信息保存到文本文件
with open('output.json', 'w', encoding='utf-8') as f:
    f.write(output_json)

print("图片信息已保存到 output.json 文件中。")
