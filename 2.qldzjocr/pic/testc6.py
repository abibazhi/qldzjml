import os
from paddleocr import PaddleOCR
from PIL import Image
from opencc import OpenCC

# 自定义裁剪函数
def custom_crop(image):
    """自定义裁剪函数"""
    width, height = image.size
    
    # 计算纵向文字区域的位置并裁剪
    left = int(width * 0.35)  # 左边界
    right = int(width * 0.65)  # 右边界
    top = int(height * 0.1)  # 上边界
    bottom = int(height * 0.9)  # 下边界
    
    cropped_image = image.crop((left, top, right, bottom))
    return cropped_image

# 初始化PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang="ch", det=True, rec=True)
# 初始化简繁转换器，配置为从繁体转简体
cc = OpenCC('t2s')

# 加载sutra.list.txt中的文本
with open('sutra.list.txt', 'r', encoding='utf-8') as file:
    sutra_lines = file.readlines()

# 遍历qldzjpng目录及其子目录
base_dir = 'qldzjpng'
for subdir in sorted(os.listdir(base_dir), key=lambda x: int(x) if x.isdigit() else float('inf')):
    subdir_path = os.path.join(base_dir, subdir)
    if os.path.isdir(subdir_path):
        # 获取当前子目录下的所有图片文件，并按文件名排序
        images = sorted([f for f in os.listdir(subdir_path) if f.endswith('.png') or f.endswith('.jpg')],
                        key=lambda x: int(os.path.splitext(x)[0]) if os.path.splitext(x)[0].isdigit() else float('inf'))
        
        for img_name in images:
            img_path = os.path.join(subdir_path, img_name)
            
            # 打开图片
            image = Image.open(img_path).convert('RGB')
            
            # 使用自定义裁剪函数裁剪出可能包含文字的纵向区域
            cropped_image = custom_crop(image)
            
            # 将裁剪后的PIL图像转换为numpy数组
            cropped_image_np = np.array(cropped_image)
            
            # 对裁剪后的图片进行文字识别
            result = ocr.ocr(cropped_image_np, cls=True)
            
            # 提取第一个文字块中的文字
            if result and result[0]:
                first_line_text = result[0][0][1][0]
                simplified_text = cc.convert(first_line_text)
                
                # 检查是否在sutra.list.txt中存在匹配
                found = False
                for idx, line in enumerate(sutra_lines):
                    if simplified_text in line:
                        print(f"匹配成功: 图片 {img_name}, 文字 '{simplified_text}', 行号 {idx + 1}")
                        found = True
                        break
                
                if not found:
                    print(f"未找到匹配: 图片 {img_name}, 文字 '{simplified_text}'")
                    # 显示裁剪后的图片以确认裁剪区域是否正确
                    cropped_image.show()
                    exit(0)
            else:
                print(f"图片 {img_name} 中未识别到任何文字")
