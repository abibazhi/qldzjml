import os
from PIL import Image
from paddleocr import PaddleOCR

# 初始化PaddleOCR，使用CPU进行推理
ocr = PaddleOCR(use_angle_cls=True, lang="ch", det=True, rec=True, precision='fp16', det_limit_side_len=640, use_gpu=False)

def process_image(img_path):
    try:
        if not os.path.exists(img_path):
            print(f"图片文件 {img_path} 不存在。")
            return

        print(f"正在处理图片: {img_path}")
        image = Image.open(img_path).convert('RGB')
        image.verify()  # 检查图片是否损坏

        width, height = image.size
        # 原代码中的裁剪区域
        original_box = (0, 0, 530, 1700)
        # 计算对称区域
        symmetric_box = (width - 530, 0, width, 1700)

        cropped_image = image.crop(symmetric_box)

        result = ocr.ocr(cropped_image, cls=True)

        text_block_count = len(result[0])  # 统计识别到的文本块总数
        recognized_texts = []

        for line in result[0]:
            recognized_text = line[1][0]
            recognized_texts.append(recognized_text)

        # 输出图片的路径名、裁剪下来图片中检测到的文本以及文本块的数量
        texts_str = '; '.join(recognized_texts)
        print(f"图片路径: {img_path}")
        print(f"检测到的文本: {texts_str}")
        print(f"文本块的数量: {text_block_count}")
        print("-" * 50)

        # 记录已处理的图片
        with open('processed_images.txt', 'a') as processed_file:
            processed_file.write(f"{img_path}\n")

    except Exception as e:
        import traceback
        print(f"处理 {img_path} 时出现错误: {traceback.format_exc()}")

def main(root_dir):
    # 读取已处理的图片列表
    processed_images = set()
    if os.path.exists('processed_images.txt'):
        with open('processed_images.txt', 'r') as processed_file:
            for line in processed_file:
                processed_images.add(line.strip())

    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg')):
                img_path = os.path.join(subdir, file)
                if img_path not in processed_images:
                    process_image(img_path)

if __name__ == "__main__":
    root_directory = "selected_images"
    main(root_directory)
