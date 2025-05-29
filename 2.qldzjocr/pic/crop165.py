import paddleocr
import numpy as np
from PIL import Image
from opencc import OpenCC

# 自定义裁剪函数
def custom_crop(image):
    """自定义裁剪函数"""
    width, height = image.size
    
    # 计算纵向文字区域的位置并裁剪
    left = int(width * 0.35)  # 左边界
    right = int(width * 0.65)  # 右边界
    top = int(height * 0.1)  # 上边界
    bottom = int(height * 0.9)  # 下边界
    
    cropped_image = image.crop((left, top, right, bottom))
    return cropped_image

# 初始化 PaddleOCR，启用文字识别
ocr = paddleocr.PaddleOCR(use_angle_cls=True, lang="ch", det=True, rec=True, precision='fp16', det_limit_side_len=640)
# 初始化简繁转换器，配置为从繁体转简体
cc = OpenCC('t2s')

# 要分析的图片路径
img_path = 'qldzjpng/001/165.png'

# 打开图片
image = Image.open(img_path).convert('RGB')

# 使用自定义裁剪函数裁剪出可能包含文字的纵向区域
cropped_image = custom_crop(image)

# 保存裁剪后的图片（可选，用于调试）
cropped_image.save("cropped_image.jpg")

# 显示裁剪后的图片以确认裁剪区域是否正确
cropped_image.show()

# 将裁剪后的PIL图像转换为numpy数组
cropped_image_np = np.array(cropped_image)

# 对裁剪后的图片进行文字识别
result = ocr.ocr(cropped_image_np, cls=True)

# 打印识别结果
print("裁剪后的识别结果：")
if result and result[0]:
    for line in result[0]:
        text = line[1][0]
        print(len(text))
        # 进行简繁转换
        simplified_text = cc.convert(text)
        print(simplified_text)
else:
    print("未识别到文字。")
