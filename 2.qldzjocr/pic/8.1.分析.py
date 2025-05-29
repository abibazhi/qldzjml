import os
import cv2
from paddleocr import PaddleOCR

# 初始化PaddleOCR，指定语言为中文
ocr = PaddleOCR(use_angle_cls=True, lang="ch")

def process_image(image_path):
    """处理单张图片并返回识别结果"""
    print(f"Processing image: {image_path}")  # 添加调试输出
    image = cv2.imread(image_path)

    if image is None:
        print(f"Failed to load image: {image_path}")  # 如果图像加载失败，打印错误信息
        return None

    # 进行文字识别
    result = ocr.ocr(image, cls=True)
    print(f"OCR Result for {image_path}: {result}")  # 打印OCR识别结果

    if len(result) > 0 and len(result[0]) > 0:
        # 获取第一个文本块
        first_text_block = result[0][0][1][0]
        return first_text_block
    else:
        return "未检测到符合条件的文本块"

def main(image_path=None):
    """
    主函数，可以接受一个图片路径参数进行单独处理。
    如果没有给定图片路径，则遍历目录及其子目录下的所有图片。
    """
    if image_path:
        # 单独处理给定的图片路径
        relative_path = os.path.basename(image_path)
        recognized_text = process_image(image_path)
        print(f"Result for {relative_path}: {recognized_text}")
    else:
        # 遍历目录及其子目录
        root_dir = 'qldzjpng_filtered'
        image_extensions = ('.png', '.jpg', '.jpeg')
        total_images = sum([len(files) for root, dirs, files in os.walk(root_dir) if any(file.lower().endswith(image_extensions) for file in files)])
        processed_images = 0
        for root, dirs, files in os.walk(root_dir):
            # 对目录名和文件名进行排序
            dirs.sort()
            files.sort()
            for file in files:
                if file.lower().endswith(image_extensions):
                    image_path = os.path.join(root, file)
                    relative_path = os.path.relpath(image_path, root_dir)

                    # 处理图像并获取识别结果
                    recognized_text = process_image(image_path)

                    # 直接打印结果而非写入文件
                    print(f"Result for {relative_path}: {recognized_text}")

                    processed_images += 1
                    print(f"已处理 {processed_images}/{total_images} 图像: {relative_path}")

if __name__ == "__main__":
    # 示例：你可以在这里指定一个具体的图片路径来测试
    specific_image_path = "qldzjpng_filtered/040/673.png"
    # 如果你想测试整个目录，请注释掉下一行
    main(specific_image_path)
    
    # 如果想要遍历整个目录，请使用如下调用方式：
    # main()
