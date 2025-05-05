import paddleocr
import numpy as np
from PIL import Image, ImageDraw
from opencc import OpenCC

# 初始化 PaddleOCR，启用文字识别
ocr = paddleocr.PaddleOCR(use_angle_cls=True, lang="ch", det=True, rec=True, precision='fp16', det_limit_side_len=640)
# 初始化简繁转换器，配置为从繁体转简体
cc = OpenCC('t2s')

# 要分析的图片路径
img_path = 'qldzjpng/001/165.png'

# 打开图片
image = Image.open(img_path).convert('RGB')
width, height = image.size

# 计算图片横向三等分的位置
one_third_width = width // 3
middle_left = one_third_width
middle_right = 2 * one_third_width

# 裁剪中间部分的图片
middle_image = image.crop((middle_left, 0, middle_right, height))

# 保存中间部分的图片（可选，用于调试）
middle_image.save("middle_image.jpg")

# 将 PIL 图像转换为 numpy 数组
middle_image_np = np.array(middle_image)

# 对中间部分的图片进行文字识别
middle_result = ocr.ocr(middle_image_np, cls=True)

# 打印中间部分的识别结果
print("中间部分的识别结果：")
if middle_result and middle_result[0]:
    for line in middle_result[0]:
        text = line[1][0]
        print(len(text))
        # 进行简繁转换
        simplified_text = cc.convert(text)
        print(simplified_text)
else:
    print("未识别到文字。")


