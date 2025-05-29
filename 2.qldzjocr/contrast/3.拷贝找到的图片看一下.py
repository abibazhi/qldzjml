import os
import shutil

def read_file(file_path):
    """读取文件内容"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

def filter_and_copy_images(input_path, output_path, temp_dir):
    """从输入文件中过滤掉包含“没有找到”的行，并将结果写入输出文件；同时将找到的图片复制到临时目录"""
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)  # 创建临时目录，如果不存在的话
    
    with open(input_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            if "没有找到" not in line:
                outfile.write(line + '\n')  # 写入过滤后的行
                
                # 提取图片路径
                parts = line.split(' - ')
                if len(parts) > 2 and '图片路径:' in parts[2]:
                    img_path = parts[2].split(': ')[1]
                    if os.path.exists(img_path):  # 确认图片路径存在
                        # 复制图片到临时目录
                        shutil.copy(img_path, temp_dir)
                    else:
                        print(f"警告: 图片路径 {img_path} 不存在.")

# 设置文件路径
input_path = './comparison_result.txt'
output_path = './filtered_comparison_result.txt'  # 过滤后的文件保存位置
temp_dir = './temp_images/'  # 临时目录用于存放找到的图片

filter_and_copy_images(input_path, output_path, temp_dir)
print(f"Filtered TXT output has been saved to {output_path}")
print(f"Copied images to {temp_dir}")
