import os
import paddleocr
import shutil

# 初始化 PaddleOCR，仅启用文本检测，禁用文字识别
ocr = paddleocr.PaddleOCR(use_angle_cls=True, lang="ch", det=True, rec=False, det_limit_side_len=640, ir_optim=False, use_tensorrt=False)

# 要分析的图片目录路径
image_dir = 'qldzjpng/078'

# 目标目录用于存储满足条件的图片
target_dir = 'qldzjpng_filtered/078'
os.makedirs(target_dir, exist_ok=True)  # 创建目标目录，如果不存在的话

# 遍历目录中的所有 PNG 图片
for filename in os.listdir(image_dir):
    if filename.endswith('.png'):
        img_path = os.path.join(image_dir, filename)
        
        # 检查图片大小是否大于50KB
        file_size_kb = os.path.getsize(img_path) / 1024
        if file_size_kb <= 50:
            continue

        # 执行版面分析（仅检测文本块）
        result = ocr.ocr(img_path, cls=True)

        # 计算文本块总数
        text_block_count = len(result[0]) if result and result[0] else 0

        # 仅当文本块数目小于 10 时记录信息并拷贝图片
        if text_block_count < 10:
            print(f"图片名称: {filename}")
            print(f"检测到的文本块总数: {text_block_count}")
            print(f"文件大小: {file_size_kb:.2f} KB")
            print("-" * 50)
            
            # 拷贝图片到目标目录
            shutil.copy(img_path, os.path.join(target_dir, filename))
            print(f"已复制 {filename} 到 {target_dir}\n")

print("所有符合条件的图片处理完毕。")
