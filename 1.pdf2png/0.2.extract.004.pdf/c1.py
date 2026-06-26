from PIL import Image

def convert_image(input_path, output_path):
    # 打开并转为灰度
    img = Image.open(input_path).convert('L')
    
    # 转为二值图（1-bit）
    binary_img = img.convert('1')  # 使用默认阈值（128）

    # 保存为高度压缩的 PNG
    binary_img.save(
        output_path,
        dpi=(96, 96),
        optimize=True,
        compress_level=9
    )
    print(f"已成功转换并保存为 {output_path}")

# 使用示例
input_file = "637mod.png"
output_file = "637.png"
convert_image(input_file, output_file)
