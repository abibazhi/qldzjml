import os
import tempfile
from PIL import Image, ImageDraw, ImageStat
from paddleocr import PaddleOCR

# 初始化PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang="ch", det=True, rec=True, precision='fp16', det_limit_side_len=640)

def detect_text_background(cropped_image):
    """ 分析给定图像区域的颜色分布，返回背景类型 """
    gray_image = cropped_image.convert('L')
    stat = ImageStat.Stat(gray_image)
    mean_value = stat.mean[0]
    if mean_value < 128:
        return "Dark background with light text"
    else:
        return "Light background with dark text"

def process_image(img_path, temp_dir_base):
    try:
        print(f"正在处理图片: {img_path}")
        image = Image.open(img_path).convert('RGB')
        width, height = image.size
        box = (0, 0, 530, 1700)  # 根据需要调整裁剪区域
        cropped_image = image.crop(box)

        # 创建临时文件夹，按子目录结构存放
        subdir_name = os.path.dirname(os.path.relpath(img_path, start=root_directory))
        temp_dir = os.path.join(temp_dir_base, subdir_name)
        os.makedirs(temp_dir, exist_ok=True)

        # 创建临时文件
        with tempfile.NamedTemporaryFile(suffix=".png", delete=True) as temp_file:
            cropped_image.save(temp_file.name)
            result = ocr.ocr(temp_file.name, cls=True)

        draw = ImageDraw.Draw(cropped_image)

        text_block_count = len(result[0])  # 统计识别到的文本块总数

        for idx, line in enumerate(result[0]):
            points = line[0]
            recognized_text = line[1][0]

            adjusted_points = [(point[0] + box[0], point[1] + box[1]) for point in points]
            x_coords = [point[0] for point in adjusted_points]
            y_coords = [point[1] for point in adjusted_points]
            cropped_text_block = image.crop((min(x_coords), min(y_coords), max(x_coords), max(y_coords)))

            background_type = detect_text_background(cropped_text_block)
            print(f"文本 {idx + 1}: {recognized_text} 的背景类型: {background_type}")

            if background_type == "Dark background with light text":
                with open(os.path.join(temp_dir_base, 'dark_background_files.txt'), 'a') as file:
                    file.write(f"图片路径: {img_path}, 文本: {recognized_text}, 识别到的文本块总数: {text_block_count}\n")

                int_points = [(int(point[0]), int(point[1])) for point in adjusted_points]
                flat_points = [coord for point in int_points for coord in point]

                draw.polygon(flat_points, outline="red")
                text_x = max(int_points[0][0], 0)
                text_y = max(int_points[0][1], 0)
                draw.text((text_x, text_y), f"{idx + 1}: {background_type}", fill="red")

                # 只有当背景为深色时才保存带有标注框的图片
                original_filename = os.path.basename(img_path)
                output_image_path = os.path.join(temp_dir, f"{original_filename.split('.')[0]}_with_boxes.jpg")
                cropped_image.save(output_image_path)

        # 记录已处理的图片
        with open(os.path.join(temp_dir_base, 'processed_images.txt'), 'a') as processed_file:
            processed_file.write(f"{img_path}\n")

    except Exception as e:
        print(f"处理 {img_path} 时出现错误: {e}")

def main(root_dir, temp_dir_base):
    # 读取已处理的图片列表
    processed_images = set()
    processed_file_path = os.path.join(temp_dir_base, 'processed_images.txt')
    if os.path.exists(processed_file_path):
        with open(processed_file_path, 'r') as processed_file:
            for line in processed_file:
                processed_images.add(line.strip())

    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg')):
                img_path = os.path.join(subdir, file)
                if img_path not in processed_images:
                    process_image(img_path, temp_dir_base)

if __name__ == "__main__":
    root_directory = "qldzjpng"
    temp_directory_base = "temp_images"
    if not os.path.exists(temp_directory_base):
        os.makedirs(temp_directory_base)
    main(root_directory, temp_directory_base)
