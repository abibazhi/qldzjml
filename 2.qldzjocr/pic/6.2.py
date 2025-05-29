import os
import cv2
from paddleocr import PaddleOCR

# 初始化PaddleOCR，指定语言为中文
ocr = PaddleOCR(use_angle_cls=True, lang="ch")

# 定义图片文件扩展名
image_extensions = ('.png', '.jpg', '.jpeg')

# 结果保存文件
output_file = 'recognition_results.txt'

def write_result(f, relative_path, text):
    """将结果写入文件并打印信息"""
    line = f"{relative_path}：{text}\n"
    f.write(line)
    print(f"已处理 {relative_path}，识别文字：{text}")

# 打开文件以写入模式
with open(output_file, 'w', encoding='utf-8') as f:
    # 遍历目录及其子目录
    root_dir = 'qldzjpng_filtered'
    total_images = sum([len(files) for root, dirs, files in os.walk(root_dir) if any(file.lower().endswith(image_extensions) for file in files)])
    processed_images = 0
    for root, dirs, files in os.walk(root_dir):
        # 对目录名和文件名进行排序
        dirs.sort()
        files.sort()
        for file in files:
            if file.lower().endswith(image_extensions):
                image_path = os.path.join(root, file)
                image = cv2.imread(image_path)

                # 进行文字识别
                result = ocr.ocr(image, cls=True)

                found_text_block = None
                # 检查每个文本块，寻找符合条件的文本块
                if len(result) > 0 and len(result[0]) > 1:
                    for i, (boxes, text_info) in enumerate(result[0]):
                        text = text_info[0]
                        if text.endswith('經'):  # 繁体"经"
                            found_text_block = text
                            break
                        elif i < 2:  # 如果是第二或第三个文本块
                            found_text_block = text_info[0]

                relative_path = os.path.relpath(image_path, root_dir)
                if found_text_block is not None:
                    # 拆分文本块中的内容，如果存在分隔符
                    texts = []
                    separators = ['丶', '、']
                    current_text = ''
                    for char in found_text_block:
                        if char in separators:
                            if current_text:
                                texts.append(current_text)
                                current_text = ''
                        else:
                            current_text += char
                    if current_text:
                        texts.append(current_text)

                    # 写入拆分后的每一项
                    for t in texts:
                        write_result(f, relative_path, t)
                else:
                    write_result(f, relative_path, "未检测到符合条件的文本块")

                processed_images += 1

print(f"识别结果已保存到 {output_file}")
