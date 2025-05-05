import cv2
import numpy as np
from paddleocr import PaddleOCR

# 初始化PaddleOCR，指定语言为中文
ocr = PaddleOCR(use_angle_cls=True, lang="ch")

# 读取图片
image_path = './qldzjpng_filtered/014/525.png'  # 替换为实际图片路径
image = cv2.imread(image_path)

# 进行文字识别
result = ocr.ocr(image, cls=True)

# 假设识别结果中第二个字不能识别，这里尝试截取第二个字所在区域
if len(result) > 0:
    words = result[0]
    if len(words) > 1:
        second_word_box = np.array(words[0][0])  # 将列表转换为numpy数组
        x, y, w, h = cv2.boundingRect(second_word_box.astype(int))  # 计算包围框
        cropped_image = image[y:y + h, x:x + w]  # 截取第二个字所在区域的图像
        cv2.imwrite('cropped_word0.jpg', cropped_image)  # 保存截取的图像
        print("第二个字所在区域已截取并保存为cropped_word.jpg")
    else:
        print("未检测到足够的文字")
else:
    print("未检测到文字")
