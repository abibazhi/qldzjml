import os
import shutil

def is_ascii(s):
    """检查字符串是否全部由ASCII字符组成"""
    return all(ord(c) < 128 for c in s)

def filter_non_ascii_and_short_lines(input_path, output_path, dest_img_dir, base_dir):
    """过滤掉文本为纯ASCII码和长度小于等于2的行，并去除空行；同时拷贝对应图片并重命名"""
    if not os.path.exists(dest_img_dir):
        os.makedirs(dest_img_dir)  # 创建目标图片目录，如果不存在的话

    with open(input_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            line = line.strip()
            if not line:  # 跳过空行
                continue
            
            parts = line.split(", 文本: ")
            if len(parts) == 2:
                img_path, text = parts
                # 过滤掉纯ASCII和长度小于等于2的文本
                if not is_ascii(text) and len(text.strip()) > 2:
                    outfile.write(f"{img_path}, 文本: {text}\n")
                    
                    # 构造新的图片名称并复制图片
                    # 确保路径是相对于基础目录的相对路径
                    absolute_img_path = os.path.join(base_dir, img_path.replace("图片路径: ", "").strip())
                    relative_path_parts = img_path.replace("图片路径: ", "").strip().split(os.sep)
                    new_img_name = "_".join(relative_path_parts) + os.path.splitext(img_path)[1]
                    dest_img_path = os.path.join(dest_img_dir, new_img_name)
                    
                    print(f"尝试复制图片: {absolute_img_path} 到 {dest_img_path}")
                    
                    if os.path.exists(absolute_img_path):
                        shutil.copy(absolute_img_path, dest_img_path)
                    else:
                        print(f"警告: 图片路径 {absolute_img_path} 不存在.")

# 设置文件路径
input_path = './1.2.dark_background_files_simplified.txt'
output_path = './filtered_dark_background_files_simplified.txt'  # 过滤后的文件保存位置
dest_img_dir = './filtered_images/'  # 过滤后图片保存的位置
base_dir = '/home/jm/dev/qldzjocr/contrast/'  # 基础目录，所有图片路径都是相对于这个目录的

filter_non_ascii_and_short_lines(input_path, output_path, dest_img_dir, base_dir)
print(f"Filtered TXT output has been saved to {output_path}")
print(f"Copied images to {dest_img_dir}")
