import os
import paddleocr
from PIL import Image

# 初始化 PaddleOCR，启用文本检测和文字识别
ocr = paddleocr.PaddleOCR(use_angle_cls=True, lang="ch", det=True, rec=True, precision='fp16', det_limit_side_len=640, use_gpu=False)

# 指定要分析的子目录
sub_dir = 'qldzjpng/028'

# 记录满足条件结果的文件
result_file = 'special_condition_results.txt'


def detect_text_in_image_part(image_part):
    """ 检测图片某一部分是否有文本 """
    result = ocr.ocr(image_part, cls=True)
    return len(result[0]) > 0


# 遍历指定子目录下的所有图片文件
for root, dirs, files in os.walk(sub_dir):
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(root, file)
            try:
                # 检查图片是否损坏
                image = Image.open(img_path).convert('RGB')
                image.verify()

                width, height = image.size

                # 横向三等分图片
                left_width = width // 3
                middle_width = 2 * left_width
                left_part = image.crop((0, 0, left_width, height))
                middle_part = image.crop((left_width, 0, middle_width, height))
                right_part = image.crop((middle_width, 0, width, height))

                # 检测各部分是否有文本
                has_text_left = detect_text_in_image_part(left_part)
                has_text_middle = detect_text_in_image_part(middle_part)
                has_text_right = detect_text_in_image_part(right_part)

                # 判断是否满足条件
                if (has_text_left and not has_text_right) or (not has_text_left and not has_text_right and has_text_middle):
                    with open(result_file, 'a', encoding='utf-8') as f:
                        f.write(f'{img_path}\n')

                print(f'Processed: {img_path}')

            except Exception as e:
                print(f"Error processing {img_path}: {e}")

print("Processing completed.")
