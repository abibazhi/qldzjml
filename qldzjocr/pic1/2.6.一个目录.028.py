# 此代码用于处理指定子目录下的图片文件，对图片进行横向三等分后检测各部分文本情况，根据特定条件筛选出符合要求的图片并记录其路径。
# 具体处理步骤和功能如下：
# 1. 图片三等分：使用 Image.crop 方法将图片横向三等分，分别得到左、中、右三个部分。
# 2. 文本检测：定义了 detect_text_in_image_part 函数，用于检测图片某一部分是否有文本。该函数调用 PaddleOCR 进行文本检测，并根据检测结果判断是否有文本。
# 3. 条件判断：根据左、中、右三个部分的文本检测结果，判断该图片是否满足设定的条件（最左面的 1/3 有文本，而最右面的 1/3 没有文本；或者最左面和最右面的图片都没有文字，中间如有文字）。若满足条件，则将图片的路径写入 result_file。
# 4. 异常处理：在处理图片时，使用 try - except 块捕获可能出现的异常，并打印错误信息。
# 注意事项：请确保将 sub_dir 替换为实际的子目录名，运行代码后，满足条件的图片路径将被记录在 special_condition_results.txt 文件中。

import os
import paddleocr
from PIL import Image

# 初始化 PaddleOCR，启用文本检测和文字识别
ocr = paddleocr.PaddleOCR(use_angle_cls=True, lang="ch", det=True, rec=True, precision='fp16', det_limit_side_len=640)

# 指定要分析的子目录
sub_dir = 'qldzjpng/028'  # 请将 'your_sub_directory' 替换为实际的子目录名

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
                # 打开图片
                image = Image.open(img_path).convert('RGB')
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
