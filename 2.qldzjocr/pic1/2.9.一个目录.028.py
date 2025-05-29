import os
from PIL import Image
from paddleocr import PaddleOCR

# 初始化PaddleOCR（确保设置use_gpu为True）
ocr = PaddleOCR(use_angle_cls=True, lang="ch", use_gpu=True)

def detect_text_in_image_part(image_path, part):
    """
    检测图片指定部分是否存在文本。
    :param image_path: 图片路径。
    :param part: 图片的部分（左、中、右）。
    :return: 如果有文本返回True，否则False。
    """
    try:
        # 打开图片并裁剪
        img = Image.open(image_path)
        width, height = img.size
        if part == 'left':
            box = (0, 0, width//3, height)
        elif part == 'middle':
            box = (width//3, 0, 2*width//3, height)
        else:  # right
            box = (2*width//3, 0, width, height)
        
        cropped_img = img.crop(box)
        cropped_img.save(f"temp_{part}.jpg")  # 临时保存裁剪后的图片
        
        # 使用PaddleOCR进行文本检测
        result = ocr.ocr(f"temp_{part}.jpg", cls=True)
        
        # 根据检测结果判断是否有文本
        if len(result[0]) > 0:  # 如果检测到了文本
            return True
        else:
            return False
    except Exception as e:
        print(f"处理 {image_path} 的 {part} 部分时出错: {e}")
        return False

def process_images_in_directory(sub_dir, result_file='special_condition_results.txt'):
    """
    处理子目录下的所有图片文件，筛选符合特定条件的图片。
    """
    with open(result_file, 'w') as f:
        for filename in os.listdir(sub_dir):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                filepath = os.path.join(sub_dir, filename)
                left_has_text = detect_text_in_image_part(filepath, 'left')
                middle_has_text = detect_text_in_image_part(filepath, 'middle')
                right_has_text = detect_text_in_image_part(filepath, 'right')

                # 判断是否满足条件
                if (left_has_text and not right_has_text) or (not left_has_text and not right_has_text and middle_has_text):
                    f.write(f"{filepath}\n")

if __name__ == "__main__":
    sub_dir = "./qldzjpng/028/"  # 替换为实际的子目录路径
import os
    process_images_in_directory(sub_dir)
