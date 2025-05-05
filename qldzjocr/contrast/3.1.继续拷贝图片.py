import os
import shutil

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
                parts = line.split(' - 图片路径: ')
                if len(parts) == 2:
                    img_path = parts[1].strip()
                    if os.path.exists(img_path):  # 确认图片路径存在
                        # 复制图片到临时目录
                        shutil.copy(img_path, temp_dir)
                    else:
                        print(f"警告: 图片路径 {img_path} 不存在.")

# 设置文件路径
input_path = './filtered_comparison_result.txt'  # 假设这是过滤后的文件路径
output_path = './final_filtered_comparison_result.txt'  # 过滤后的文件保存位置
temp_dir = './temp_images/'  # 临时目录用于存放找到的图片

filter_and_copy_images(input_path, output_path, temp_dir)
print(f"Filtered TXT output has been saved to {output_path}")
print(f"Copied images to {temp_dir}")
