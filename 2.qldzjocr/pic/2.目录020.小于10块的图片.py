import os
import paddleocr
import logging

# 设置日志级别为 ERROR，抑制调试信息输出
logging.getLogger('ppocr').setLevel(logging.ERROR)

# 初始化 PaddleOCR，仅启用文本检测，禁用文字识别
ocr = paddleocr.PaddleOCR(use_angle_cls=True, lang="ch", det=True, rec=False, det_limit_side_len=640, ir_optim=False, use_tensorrt=False)

# 要分析的图片目录路径
image_dir = 'qldzjpng/020'

# 用于存储满足条件的图片信息
output_info = []

# 遍历目录中的所有 PNG 图片
for filename in os.listdir(image_dir):
    if filename.endswith('.png'):
        img_path = os.path.join(image_dir, filename)

        # 执行版面分析（仅检测文本块）
        result = ocr.ocr(img_path, cls=True)

        # 计算文本块总数
        text_block_count = len(result[0])

        # 仅当文本块数目小于 10 时记录信息
        if text_block_count < 10:
            info = f"图片名称: {filename}\n检测到的文本块总数: {text_block_count}\n" + "-" * 50
            output_info.append(info)

# 一次性打印所有满足条件的图片信息
for info in output_info:
    print(info)
