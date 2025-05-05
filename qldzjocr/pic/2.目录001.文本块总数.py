import os
import paddleocr

# 初始化 PaddleOCR，仅启用文本检测，禁用文字识别
ocr = paddleocr.PaddleOCR(use_angle_cls=True, lang="ch", det=True, rec=False, det_limit_side_len=640, ir_optim=False, use_tensorrt=False)

# 要分析的图片目录路径
image_dir = 'qldzjpng/001'

# 遍历目录中的所有 PNG 图片
for filename in os.listdir(image_dir):
    if filename.endswith('.png'):
        img_path = os.path.join(image_dir, filename)

        # 执行版面分析（仅检测文本块）
        result = ocr.ocr(img_path, cls=True)

        # 计算文本块总数
        text_block_count = len(result[0])

        print(f"图片名称: {filename}")
        print(f"检测到的文本块总数: {text_block_count}")

        print("-" * 50)
