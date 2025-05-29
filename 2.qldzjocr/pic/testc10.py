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
        second_word_box = np.array(words[1][0])  # 将列表转换为numpy数组
        x, y, w, h = cv2.boundingRect(second_word_box.astype(int))  # 计算包围框
        cropped_image = image[y:y + h, x:x + w]  # 截取第二个字所在区域的图像
        cv2.imwrite('cropped_word.jpg', cropped_image)  # 保存截取的图像
        print("第二个字所在区域已截取并保存为cropped_word.jpg")

        # 对截取的图片再次进行文字识别
        sub_result = ocr.ocr(cropped_image, cls=True)
        if len(sub_result) > 0 and len(sub_result[0]) > 1:
            # 截取第二个字符
            second_char_box = np.array(sub_result[0][1][0])
            sub_x, sub_y, sub_w, sub_h = cv2.boundingRect(second_char_box.astype(int))
            sub_cropped_image = cropped_image[sub_y:sub_y + sub_h, sub_x:sub_x + sub_w]
            cv2.imwrite('second_char.jpg', sub_cropped_image)
            print("截取图片中的第二个字符已保存为second_char.jpg")
        else:
            print("截取的图片中未检测到足够的字符")
    else:
        print("未检测到足够的文字")
else:
    print("未检测到文字")
