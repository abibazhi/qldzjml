def read_file(file_path):
    """读取文件内容"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

def build_image_dict(image_text_path):
    """构建图像文本映射表"""
    images_texts = read_file(image_text_path)
    image_dict = {}
    start_indices = []
    current_index = 0
    for line in images_texts:
        parts = line.split(", 文本: ")
        if len(parts) == 2:  # 确保分割得到两个部分
            img_path = parts[0]
            text = parts[1]
            image_dict[text] = img_path
            start_indices.append((current_index, img_path))
            current_index += len(text) + 1  # 加1是为了考虑换行符
    return image_dict, start_indices

def similar_match_search(sutra, image_dict, start_indices, match_threshold=5):
    """尝试相似匹配搜索"""
    matches = []
    sutra_len = len(sutra)

    last_matched_index = 0
    for i, (start_index, img_path) in enumerate(start_indices):
        if start_index < last_matched_index:
            continue  # 跳过已经检查过的部分
        
        target_text = list(image_dict.keys())[i]
        target_len = len(target_text)

        max_length = max(sutra_len, target_len)
        count = 0

        for j in range(max_length):
            if j < sutra_len and j < target_len and sutra[j] == target_text[j]:
                count += 1
                if count >= match_threshold:
                    matches.append((f"相似匹配 - {target_text[:j+1]}", img_path, start_index))
                    last_matched_index = start_index + j + 1  # 更新最后匹配的位置
                    break
            else:
                count = 0

    return matches

def refine_comparison(comparison_result_path, image_text_path, refined_output_path):
    """基于初始比较结果进行细化检查，并输出新结果"""
    comparison_results = read_file(comparison_result_path)
    image_dict, start_indices = build_image_dict(image_text_path)

    refined_output = ""
    
    for line in comparison_results:
        if "没有找到" in line:
            sutra = line.split(" - ")[0]
            matches = similar_match_search(sutra, image_dict, start_indices)
            if matches:
                for match_info, img_path, start_index in matches:
                    refined_output += f"{sutra} - {match_info} - {img_path} (起始位置: {start_index})\n"
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
