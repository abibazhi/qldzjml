import os
import paddleocr
import logging
import json

# 配置日志记录
logging.basicConfig(filename='processing.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# 设置日志级别为 ERROR，抑制调试信息输出
logging.getLogger('ppocr').setLevel(logging.ERROR)

# 初始化 PaddleOCR，仅启用文本检测，禁用文字识别
ocr = paddleocr.PaddleOCR(use_angle_cls=True, lang="ch", det=True, rec=False, det_limit_side_len=640, ir_optim=False, use_tensorrt=False)

# 要分析的根图片目录路径
image_dir = 'qldzjpng'

# 用于存储所有图片信息的字典
all_info = {}

# 检查 output.json 文件是否存在，如果存在则加载之前的结果
if os.path.exists('output.json'):
    with open('output.json', 'r', encoding='utf-8') as f:
        all_info = json.load(f)

# 记录已经处理过的目录
processed_dirs = set(all_info.keys())

# 递归遍历目录及其子目录
for root, dirs, files in os.walk(image_dir):
    # 获取当前目录相对于根目录的相对路径作为目录名
    relative_dir = os.path.relpath(root, image_dir)
    if relative_dir == '.':
        relative_dir = ''
    # 跳过已经处理过的目录
    if relative_dir in processed_dirs:
        continue
    # 存储当前目录下的图片信息
    dir_info = {}
    for filename in files:
        if filename.endswith('.png'):
            img_path = os.path.join(root, filename)
            try:
                # 执行版面分析（仅检测文本块）
                result = ocr.ocr(img_path, cls=True)
                if result is None:
                    # 记录返回 None 的情况
                    logging.warning(f"目录名: {relative_dir}, 文件名: {filename}, 检测结果为 None")
                    continue
                # 计算文本块总数
                text_block_count = len(result[0])
                # 仅当文本块数目小于 10 时记录信息并输出到控制台和日志
                if text_block_count < 10:
                    # 记录文件名及其对应的文本块数量
                    dir_info[filename] = text_block_count
                    # 输出当前图片的处理结果到控制台
                    print(f"目录名: {relative_dir}, 文件名: {filename}, 文件块数: {text_block_count}")
                    # 记录到日志文件
                    logging.info(f"目录名: {relative_dir}, 文件名: {filename}, 文件块数: {text_block_count}")
            except Exception as e:
                # 记录异常信息
                logging.error(f"目录名: {relative_dir}, 文件名: {filename}, 处理出错: {str(e)}")
    if dir_info:
        all_info[relative_dir] = dir_info
    # 每次处理完一个目录后，保存当前的结果到 output.json
    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(all_info, f, indent=4, ensure_ascii=False)
    # 将当前目录标记为已处理
    processed_dirs.add(relative_dir)

print("图片信息已保存到 output.json 文件中。")
