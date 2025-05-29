import os
import zipfile
from pathlib import Path

def unzip_to_individual_dirs(zip_files, output_dir):
    """
    将多个zip文件分别解压到以其名称命名的独立目录中，并置于输出目录下。
    
    :param zip_files: 要解压的zip文件列表
    :param output_dir: 输出目录，用于存放解压后的文件夹
    """
    for zip_file in zip_files:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            # 使用zip文件名（不含扩展名）作为解压目录名
            target_dir = os.path.join(output_dir, os.path.splitext(os.path.basename(zip_file))[0])
            # 如果目录不存在，则创建
            os.makedirs(target_dir, exist_ok=True)
            # 解压缩文件到目标目录
            zip_ref.extractall(target_dir)
            print(f"已解压 {zip_file} 到 {target_dir}")

def main():
    # 设置要操作的目录和临时目录
    source_dir = "/mnt/d/qldzj/qldzjpng.zip"
    temp_output_dir = "/mnt/d/qldzj/unzipped_temp"

    # 获取源目录下所有的zip文件
    zip_files = list(Path(source_dir).glob('*.zip'))

    if not zip_files:
        print("没有找到任何zip文件")
        return

    # 创建临时目录
    Path(temp_output_dir).mkdir(parents=True, exist_ok=True)

    # 解压缩并处理
    unzip_to_individual_dirs(zip_files, temp_output_dir)

if __name__ == "__main__":
    main()
