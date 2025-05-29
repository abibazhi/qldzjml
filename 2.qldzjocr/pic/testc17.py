import cv2
import numpy as np
from paddleocr import PaddleOCR

# 初始化PaddleOCR，指定语言为中文
ocr = PaddleOCR(use_angle_cls=True, lang="ch")

# 读取图片
image_path = "qldzjpng_filtered/014/525.png"
image = cv2.imread(image_path, 0)  # 以灰度模式读取

# 形态学操作：先膨胀后腐蚀，增强文本的连通性
kernel = np.ones((3, 3), np.uint8)
image = cv2.dilate(image, kernel, iterations=1)
image = cv2.erode(image, kernel, iterations=1)

# 进行文字识别
result = ocr.ocr(image, cls=True)

if result:
    for i, line in enumerate(result[0]):
        word_box = np.array(line[0])
        x, y, w, h = cv2.boundingRect(word_box.astype(int))
        cropped_image = image[y:y + h, x:x + w]

        # 提取当前文本块识别出的文字
        recognized_text = line[1][0]
        char_count = len(recognized_text)

        if char_count > 0:
            # 计算每个字符的宽度
            char_width = w // char_count

            for j in range(char_count):
                start_x = x + j * char_width
                end_x = start_x + char_width
                single_char_image = cropped_image[:, start_x - x:end_x - x]
                file_name = f'text_block_{i + 1}_char_{j + 1}.jpg'
                cv2.imwrite(file_name, single_char_image)
                print(f"第 {i + 1} 个文本块的第 {j + 1} 个字符已保存为 {file_name}，字符为: {recognized_text[j]}")
else:
    print("未检测到文本块")
