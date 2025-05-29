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

def partial_match_search(sutra, image_dict):
    """尝试部分匹配搜索"""
    matches = []
    # 从末尾逐步减少字符
    for i in range(len(sutra), 3, -1):  
        part_sutra = sutra[:i]
        if part_sutra in image_dict:
            matches.append(("部分匹配(从左)-" + part_sutra, image_dict[part_sutra]))
    
    # 从开头逐步减少字符
    for i in range(len(sutra), 3, -1):  
        part_sutra = sutra[-i:]
        if part_sutra in image_dict:
            matches.append(("部分匹配(从右)-" + part_sutra, image_dict[part_sutra]))
    
    return matches

def refine_comparison(comparison_result_path, image_text_path, refined_output_path):
    """基于初始比较结果进行细化检查，并输出新结果"""
    comparison_results = read_file(comparison_result_path)
    image_dict = build_image_dict(image_text_path)

    refined_output = ""
    
    for line in comparison_results:
        if "没有找到" in line:
            sutra = line.split(" - ")[0]
            matches = partial_match_search(sutra, image_dict)
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
