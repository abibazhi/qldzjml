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
            image_dict[current_index] = {'text': text, 'img_path': img_path}
            start_indices.append(current_index)
            current_index += len(text) + 1  # 加1是为了考虑换行符
    return image_dict, start_indices

def find_next_match(sutra_line, image_dict, start_indices, search_start=0, match_threshold=5):
    """从指定位置开始查找下一个匹配项"""
    sutra_len = len(sutra_line)
    
    for index in start_indices:
        if index < search_start:
            continue  # 跳过已经检查过的部分
        
        target_text = image_dict[index]['text']
        target_len = len(target_text)

        max_length = max(sutra_len, target_len)
        count = 0

        for j in range(max_length):
            if j < sutra_len and j < target_len and sutra_line[j] == target_text[j]:
                count += 1
                if count >= match_threshold:
                    return index, image_dict[index]['img_path'], index + len(target_text)  # 返回匹配索引、图片路径和结束位置
            else:
                count = 0
                
    return None, None, None  # 如果没有找到匹配项

def refine_comparison(comparison_result_path, image_text_path, refined_output_path):
    """基于初始比较结果进行细化检查，并输出新结果"""
    comparison_results = read_file(comparison_result_path)
    image_dict, start_indices = build_image_dict(image_text_path)
    search_start = 0  # 初始化搜索起点

    refined_output = ""
    
    for line in comparison_results:
        if "没有找到" in line:
            sutra_line = line.split(" - ")[0]
            match_index, img_path, next_search_start = find_next_match(sutra_line, image_dict, start_indices, search_start)
            
            if match_index is not None:
                refined_output += f"{sutra_line} - 相似匹配 - {image_dict[match_index]['text']} - {img_path} (起始位置: {match_index})\n"
                search_start = next_search_start  # 更新搜索起点为最后一个匹配位置之后
            else:
                refined_output += f"{sutra_line} - 没有找到\n"
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
