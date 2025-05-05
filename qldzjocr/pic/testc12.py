import cv2
import numpy as np
from paddleocr import PaddleOCR


# 初始化PaddleOCR，指定语言为中文
ocr = PaddleOCR(use_angle_cls=True, lang="ch")
# 读取图片
image_path = "qldzjpng_filtered/014/525.png"
image = cv2.imread(image_path)

# 进行文字识别
result = ocr.ocr(image, cls=True)

if len(result) >= 1:
    # 保存第一个文本块
    first_word_box = np.array(result[0][0][0])
    x1, y1, w1, h1 = cv2.boundingRect(first_word_box.astype(int))
    cropped_image = image[y1:y1 + h1, x1:x1 + w1]
    if len(result) == 1:
        cv2.imwrite('single_text_block.jpg', cropped_image)
        print("仅检测到一个文本块，已保存为single_text_block.jpg")
    else:
        cv2.imwrite('first_text_block.jpg', cropped_image)
        print("第一个文本块已保存为first_text_block.jpg")
        # 保存第二个文本块
        second_word_box = np.array(result[0][1][0])
        x2, y2, w2, h2 = cv2.boundingRect(second_word_box.astype(int))
        cropped_image2 = image[y2:y2 + h2, x2:x2 + w2]
        cv2.imwrite('second_text_block.jpg', cropped_image2)
        print("第二个文本块已保存为second_text_block.jpg")
else:
    print("未检测到文本块")
