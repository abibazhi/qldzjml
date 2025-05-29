import os
import shutil

# 定义源文件和目标临时目录
source_base_dir = './'  # 假设这是基础目录，根据实际情况调整
temp_dir = './selected_images'
os.makedirs(temp_dir, exist_ok=True)  # 创建临时目录

# 读取文件并处理
with open('dark_background_files.txt', 'r', encoding='utf-8') as file:
    for line in file:
        parts = line.split(', 文本: ')
        if len(parts) < 2: continue  # 格式不正确则跳过
        img_info_part, text_block_part = parts
        path_part = img_info_part.split('图片路径: ')[1]
        total_text_blocks = int(text_block_part.split('识别到的文本块总数: ')[1])

        if total_text_blocks == 1:
            # 构建原文件的完整路径以及新的文件名
            full_path = os.path.join(source_base_dir, path_part.strip())
            relative_path = os.path.relpath(full_path, source_base_dir)
            new_filename = relative_path.replace(os.sep, '_')
            new_full_path = os.path.join(temp_dir, new_filename)

            # 复制文件到临时目录，并重命名
            try:
                shutil.copy2(full_path, new_full_path)
                print(f"已复制并重命名 {full_path} 至 {new_full_path}")
            except FileNotFoundError:
                print(f"文件未找到: {full_path}")
            except Exception as e:
                print(f"复制文件时出错: {e}")
