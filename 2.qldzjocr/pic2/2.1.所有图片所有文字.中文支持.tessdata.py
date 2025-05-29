import os
from PIL import Image
import pytesseract

# 设置 TESSDATA_PREFIX 环境变量指向你的 tessdata 目录
os.environ['TESSDATA_PREFIX'] = '/home/jm/dev/qldzjocr/pic2/tessdata/'  # 根据实际情况修改路径

def process_image(image_path):
    """处理单张图像，返回文件名、文字块数量以及全部文字"""
    image = Image.open(image_path)
    
    # 使用pytesseract进行OCR识别，并指定语言为中文（简体）
    data = pytesseract.image_to_data(image, lang='chi_sim', output_type=pytesseract.Output.DICT)
    
    words = []
    n_boxes = len(data['text'])
    for i in range(n_boxes):
        if int(data['conf'][i]) > 60:  # 过滤掉置信度较低的结果
            words.append(data['text'][i])
    
    return os.path.basename(image_path), len(words), ' '.join(words)

def main(selected_images_dir, output_txt):
    """主函数：遍历目录中的所有图像，识别文字，并将结果写入txt文件"""
    with open(output_txt, 'w') as f:
        for filename in os.listdir(selected_images_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                image_path = os.path.join(selected_images_dir, filename)
                file_name, block_count, text = process_image(image_path)
                f.write(f"{file_name} {block_count} {text}\n")
                print(f"已处理: {filename}")

if __name__ == "__main__":
    selected_images_dir = './selected_images'  # 替换为你的selected_images目录路径
    output_txt = 'output.txt'  # 输出结果的txt文件路径
    main(selected_images_dir, output_txt)
