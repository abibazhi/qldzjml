import os
from PIL import Image
from paddleocr import PaddleOCR

# 初始化PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang="ch", det=True, rec=True, precision='fp16', det_limit_side_len=640)

def process_image(img_path):
    try:
        print(f"正在处理图片: {img_path}")
        with Image.open(img_path) as image:
            image = image.convert('RGB')
            width, height = image.size
            
            # 检查图像尺寸是否足够大以进行裁剪
            if width < 530 or height < 1700:
                print(f"跳过 {img_path}：图像尺寸不足")
                return
            
            # 对称的裁剪区域
            box = (width - 530, 0, width, 1700)
            cropped_image = image.crop(box)

            # OCR识别
            result = ocr.ocr(cropped_image, cls=True)

            text_block_count = len(result[0]) if result and result[0] else 0  # 统计识别到的文本块总数
            detected_texts = [line[1][0] for line in result[0]] if result and result[0] else []

            print(f"图片路径: {img_path}, 检测到的文本块总数: {text_block_count}, 文本内容: {detected_texts}")

    except Exception as e:
        print(f"处理 {img_path} 时出现错误: {str(e)}")

def main(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg')):
                img_path = os.path.join(subdir, file)
                process_image(img_path)

if __name__ == "__main__":
    root_directory = "selected_images"  # 修改为你需要遍历的目录
    main(root_directory)
