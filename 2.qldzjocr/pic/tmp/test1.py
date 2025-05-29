import paddleocr

# 初始化 PaddleOCR，选择语言模型（这里使用中文）
ocr = paddleocr.PaddleOCR(use_angle_cls=True, lang="ch")

# 要识别的图片路径
img_path = 'qldzjpng/001/167.png'

# 执行版面识别和文字识别
result = ocr.ocr(img_path, cls=True)

# 打印识别结果，包括文本框坐标、文字和识别置信度
for line in result:
    print("文本框坐标:", line[0])
    print("识别文字:", line[1][0])
    print("识别置信度:", line[1][1])
    print("----")
