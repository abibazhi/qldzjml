import os
from PIL import Image

def tiff_to_png(tiff_path, output_path=None):
    """
    将TIFF图像转换为PNG格式。
    
    :param tiff_path: 输入的TIFF文件路径。
    :param output_path: 输出的PNG文件路径。如果未指定，则在原文件名后加上.png作为新文件名。
    """
    # 打开TIFF图像
    img = Image.open(tiff_path)
    
    # 如果没有提供输出路径，则根据输入路径自动生成一个输出文件名
    if output_path is None:
        output_path = os.path.splitext(tiff_path)[0] + '.png'
    
    # 保存为PNG格式
    img.save(output_path, 'PNG')
    print(f"已将 {tiff_path} 转换为 {output_path}")

# 使用示例
current_dir = os.getcwd()
tiff_file = os.path.join(current_dir, '539.tiff')

tiff_to_png(tiff_file)
