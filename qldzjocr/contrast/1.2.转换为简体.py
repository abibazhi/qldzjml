import opencc

# 初始化OpenCC用于繁体转简体
cc = opencc.OpenCC('t2s')

def convert_to_simplified(file_path, output_file_path):
    """将指定文件中的繁体字转换为简体字，并保存结果"""
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # 转换为简体并准备写入新的文件
    simplified_lines = [cc.convert(line) for line in lines]
    
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for line in simplified_lines:
            output_file.write(line + '\n')
    
    print(f"转换完成并保存至 {output_file_path}")

# 设置文件路径
image_text_path = '/mnt/d/temp/temp_images/dark_background_files.txt'  # 文件2的路径
output_simplified_file_path = './dark_background_files_simplified.txt'  # 简体字版本保存位置

convert_to_simplified(image_text_path, output_simplified_file_path)
