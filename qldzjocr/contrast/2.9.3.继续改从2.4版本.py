import os
import shutil

def read_file(file_path):
    """读取文件内容"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

def build_image_dict(image_text_path):
    """构建图像文本映射表"""
    images_texts = read_file(image_text_path)
    image_dict = {}
    for line in images_texts:
        parts = line.split(", 文本: ")
        if len(parts) == 2:  # 确保分割得到两个部分
            img_path = parts[0]
            text = parts[1]
            image_dict[text] = img_path
    return image_dict

def similar_match_search(sutra, image_dict, used_texts):
    """尝试相似匹配搜索"""
    match_threshold = 6  # 至少需要5个连续字符匹配
    sutra_len = len(sutra)

    for target_text in image_dict.keys():
        if target_text in used_texts:  # 跳过已经使用过的文本
            continue
        
        target_len = len(target_text)
        max_length = max(sutra_len, target_len)

        for i in range(max_length):
            count = 0
            for j in range(max_length):
                if i + j < sutra_len and j < target_len and sutra[i + j] == target_text[j]:
                    count += 1
                    if count >= match_threshold:
                        used_texts.add(target_text)  # 标记为已使用
                        return ("相似匹配 - " + target_text[:j+1], image_dict[target_text])
                else:
                    count = 0
            if count >= match_threshold:
                break

    return None, None

def refine_comparison(comparison_result_path, image_text_path, refined_output_path, temp_dir):
    """基于初始比较结果进行细化检查，并输出新结果"""
    comparison_results = read_file(comparison_result_path)
    image_dict = build_image_dict(image_text_path)
    used_texts = set()  # 用于记录已经被匹配的文本

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)  # 创建临时目录，如果不存在的话

    refined_output = ""

    for line in comparison_results:
        if "没有找到" in line:
            sutra = line.split(" - ")[0]
            match_info, img_path = similar_match_search(sutra, image_dict, used_texts)
            if match_info and img_path:
                refined_output += f"{sutra} - {match_info} - 图片路径: {img_path}\n"
                # 复制图片到临时目录
                if os.path.exists(img_path):
                    shutil.copy(img_path, temp_dir)
                else:
                    print(f"警告: 图片路径 {img_path} 不存在.")
            else:
                refined_output += f"{sutra} - 没有找到\n"
        else:
            refined_output += f"{line}\n"

    with open(refined_output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(refined_output)

    print(f"Filtered TXT output has been saved to {refined_output_path}")
    print(f"Copied images to {temp_dir}")

# 设置文件路径
comparison_result_path = './comparison_result.txt'
image_text_path = './1.2.dark_background_files_simplified.txt'
refined_output_path = './filtered_comparison_result.txt'  # 过滤后的文件保存位置
temp_dir = './temp_images/'  # 临时目录用于存放找到的图片

refine_comparison(comparison_result_path, image_text_path, refined_output_path, temp_dir)
