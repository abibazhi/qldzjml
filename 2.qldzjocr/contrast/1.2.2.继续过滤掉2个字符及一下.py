import re

def is_ascii(s):
    """检查字符串是否全部由ASCII字符组成"""
    return all(ord(c) < 128 for c in s)

def filter_non_ascii_and_short_lines(input_path, output_path):
    """过滤掉文本为纯ASCII码和长度小于等于2的行，并去除空行"""
    with open(input_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            line = line.strip()
            if not line:  # 跳过空行
                continue
            
            parts = line.split(", 文本: ")
            if len(parts) == 2:
                img_path, text = parts
                # 过滤掉纯ASCII和长度小于等于2的文本
                if not is_ascii(text) and len(text.strip()) > 2:
                    outfile.write(f"{img_path}, 文本: {text}\n")

# 设置文件路径
input_path = './1.2.dark_background_files_simplified.txt'
output_path = './filtered_dark_background_files_simplified.txt'  # 过滤后的文件保存位置

filter_non_ascii_and_short_lines(input_path, output_path)
print(f"Filtered TXT output has been saved to {output_path}")
