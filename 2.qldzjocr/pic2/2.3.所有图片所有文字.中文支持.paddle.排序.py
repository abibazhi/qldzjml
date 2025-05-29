import os
from paddleocr import PaddleOCR

def process_image(ocr, image_path):
    """处理单张图像，返回文件名、文字块数量以及全部文字"""
    result = ocr.ocr(image_path, cls=True)
    
    words = []
    for line in result:
        for word_info in line:
            text = word_info[1][0]  # 获取识别出的文字
            if float(word_info[1][1]) > 0.6:  # 过滤掉置信度较低的结果
                words.append(text)
    
    return os.path.basename(image_path), len(words), ' '.join(words)

def main(selected_images_dir, output_txt):
    """主函数：遍历目录中的所有图像，识别文字，并将结果写入txt文件"""
    # 初始化PaddleOCR，可根据需要调整参数
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # 使用中文语言模型
    
    with open(output_txt, 'w') as f:
        # 获取目录中所有支持格式的图像文件并按文件名排序
        supported_exts = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')
        image_files = [f for f in os.listdir(selected_images_dir) if f.lower().endswith(supported_exts)]
        sorted_image_files = sorted(image_files)  # 按文件名排序
        
        for filename in sorted_image_files:
            image_path = os.path.join(selected_images_dir, filename)
            file_name, block_count, text = process_image(ocr, image_path)
            f.write(f"{file_name} {block_count} {text}\n")
            print(f"已处理: {filename}")

if __name__ == "__main__":
    selected_images_dir = './selected_images'  # 替换为你的selected_images目录路径
    output_txt = 'output.txt'  # 输出结果的txt文件路径
    main(selected_images_dir, output_txt)
