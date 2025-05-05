import os
import shutil
import json

# 读取 output.json 文件
with open('output.json', 'r', encoding='utf-8') as f:
    all_info = json.load(f)

# 原图片根目录
source_dir = 'qldzjpng'
# 目标目录
destination_dir = 'qldzjpng_filtered2'

# 遍历所有目录信息
for relative_dir, files_info in all_info.items():
    # 构建目标子目录路径
    target_sub_dir = os.path.join(destination_dir, relative_dir)
    # 如果目标子目录不存在，则创建它
    if not os.path.exists(target_sub_dir):
        os.makedirs(target_sub_dir)
    # 遍历当前目录下的所有符合条件的图片
    for filename in files_info.keys():
        # 构建原图片的完整路径
        source_file_path = os.path.join(source_dir, relative_dir, filename)
        # 构建目标图片的完整路径
        target_file_path = os.path.join(target_sub_dir, filename)
        try:
            # 拷贝图片
            shutil.copy2(source_file_path, target_file_path)
            print(f"已拷贝文件: {source_file_path} 到 {target_file_path}")
        except Exception as e:
            print(f"拷贝文件 {source_file_path} 时出错: {str(e)}")

print("文件拷贝完成。")
