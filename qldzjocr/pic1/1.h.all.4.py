import os
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

def process_image(img_path, temp_dir_base, completed_file):
    try:
        print(f"正在处理图片: {img_path}")
        image = Image.open(img_path).convert('RGB')
        width, height = image.size
        box = (0, 0, 530, 1700)  # 根据需要调整裁剪区域
        cropped_image = image.crop(box)

        subdir_name = os.path.dirname(os.path.relpath(img_path, start=root_directory))
        temp_dir = os.path.join(temp_dir_base, subdir_name)
        os.makedirs(temp_dir, exist_ok=True)

        original_filename = os.path.basename(img_path)
        temp_image_name = f"{original_filename.split('.')[0]}_cropped.png"
        cropped_image_path = os.path.join(temp_dir, temp_image_name)
        cropped_image.save(cropped_image_path)

        result = ocr.ocr(cropped_image_path, cls=True)
        draw = ImageDraw.Draw(cropped_image)

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
                    file.write(f"图片路径: {img_path}, 文本: {recognized_text}\n")

            int_points = [(int(point[0]), int(point[1])) for point in adjusted_points]
            flat_points = [coord for point in int_points for coord in point]

            draw.polygon(flat_points, outline="red")
            text_x = max(int_points[0][0], 0)
            text_y = max(int_points[0][1], 0)
            draw.text((text_x, text_y), f"{idx + 1}: {background_type}", fill="red")

        output_image_path = os.path.join(temp_dir, f"{original_filename.split('.')[0]}_with_boxes.jpg")
        cropped_image.save(output_image_path)

        # 将已处理的图片路径记录到completed_file
        with open(completed_file, 'a') as file:
            file.write(f"{img_path}\n")
    except Exception as e:
        print(f"处理 {img_path} 时出现错误: {e}")

def main(root_dir, temp_dir_base, completed_file):
    # 加载已完成的图片列表
    if os.path.exists(completed_file):
        with open(completed_file, 'r') as file:
            completed_images = set(line.strip() for line in file)
    else:
        completed_images = set()

    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg')):
                img_path = os.path.join(subdir, file)
                if img_path not in completed_images:  # 跳过已经处理过的图片
                    process_image(img_path, temp_dir_base, completed_file)

if __name__ == "__main__":
    root_directory = "qldzjpng"
    temp_directory_base = "temp_images"
    completed_file = "completed_images.txt"
    main(root_directory, temp_directory_base, completed_file)
