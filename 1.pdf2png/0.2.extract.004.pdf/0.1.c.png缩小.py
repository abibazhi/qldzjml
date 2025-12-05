from PIL import Image

def convert_image(input_path, output_path):
    # 打开图像并转换为灰度图
    img = Image.open(input_path).convert('L')
    
    # 进一步将灰度图转换为二值图(1-bit)
    binary_img = img.convert('1')  # 自动应用阈值
    
    # 设置目标DPI (PIL中通过设置info['dpi']来实现，但在保存时可能需要手动指定)
    binary_img.info['dpi'] = (96, 96)
    
    # 保存图像，注意dpi参数在此处不起作用，因此直接在info中设置了
    binary_img.save(output_path, dpi=binary_img.info['dpi'])
    print(f"已成功转换并保存为 {output_path}")

# 使用示例
#input_file = "532.great.png"
#output_file = "532.great.new.png"

input_file = "222.png"
output_file = "222.new.png"
convert_image(input_file, output_file)
