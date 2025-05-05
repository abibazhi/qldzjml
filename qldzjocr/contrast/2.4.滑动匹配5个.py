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

def similar_match_search(sutra, image_dict):
    """尝试相似匹配搜索"""
    matches = []
    match_threshold = 5  # 至少需要5个连续字符匹配
    sutra_len = len(sutra)

    for target_text in image_dict.keys():
        target_len = len(target_text)
        max_length = max(sutra_len, target_len)

        for i in range(max_length):
            count = 0
            for j in range(max_length):
                if i + j < sutra_len and j < target_len and sutra[i + j] == target_text[j]:
                    count += 1
                    if count >= match_threshold:
                        matches.append(("相似匹配 - " + target_text[:j+1], image_dict[target_text]))
                        break
                else:
                    count = 0
            if count >= match_threshold:
                break

    return matches

def refine_comparison(comparison_result_path, image_text_path, refined_output_path):
    """基于初始比较结果进行细化检查，并输出新结果"""
    comparison_results = read_file(comparison_result_path)
    image_dict = build_image_dict(image_text_path)

    refined_output = ""
    
    for line in comparison_results:
        if "没有找到" in line:
            sutra = line.split(" - ")[0]
            matches = similar_match_search(sutra, image_dict)
            if matches:
                for match_info, img_path in matches:
                    refined_output += f"{sutra} - {match_info} - {img_path}\n"
            else:
                refined_output += f"{sutra} - 没有找到\n"
        else:
            refined_output += f"{line}\n"

    with open(refined_output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(refined_output)

    print(f"Refined TXT output has been saved to {refined_output_path}")

# 设置文件路径
comparison_result_path = './comparison_result.txt'
image_text_path = './1.2.dark_background_files_simplified.txt'
refined_output_path = './refined_comparison_result.txt'  # 输出细化后TXT文件的位置

refine_comparison(comparison_result_path, image_text_path, refined_output_path)
