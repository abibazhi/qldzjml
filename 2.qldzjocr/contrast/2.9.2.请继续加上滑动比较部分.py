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

def sliding_compare1(sutra_line, target_text, match_threshold=5):
    """滑动比较两个字符串"""
    sutra_len = len(sutra_line)
    target_len = len(target_text)

    max_length = max(sutra_len, target_len)
    
    for i in range(max_length - min(sutra_len, target_len) + 1):
        count = 0
        for j in range(min(sutra_len, target_len)):
            if j < sutra_len and j < target_len and sutra_line[j] == target_text[i + j]:
                count += 1
        if count >= match_threshold:
            return True, count
    return False, 0

def sliding_compare(sutra_line, target_text, match_threshold=5):
    """滑动比较两个字符串"""
    sutra_len = len(sutra_line)
    target_len = len(target_text)
    
    # 确保sutra_line总是较短的一方来进行比较
    if sutra_len > target_len:
        temp = sutra_line
        sutra_line = target_text
        target_text = temp
        sutra_len = len(sutra_line)
        target_len = len(target_text)

    max_length = max(sutra_len, target_len)
    
    for i in range(max(0, target_len - sutra_len + 1)):  # 调整循环边界
        count = 0
        for j in range(sutra_len):  # 直接遍历较短字符串的长度
            if i + j < target_len and sutra_line[j] == target_text[i + j]:  # 加入边界检查
                count += 1
        if count >= match_threshold:
            return True, count
    return False, 0

def find_next_match(sutra_line, image_dict, start_indices, search_start=0, match_threshold=5):
    """从指定位置开始查找下一个匹配项"""
    best_match = None
    best_count = 0
    next_search_start = search_start
    
    for index in start_indices:
        if index < search_start:
            continue
        
        target_text = image_dict[index]['text']
        is_match, match_count = sliding_compare(sutra_line, target_text, match_threshold)
        
        if is_match and match_count > best_count:
            best_match = (index, image_dict[index]['img_path'])
            best_count = match_count
            next_search_start = index + len(target_text)
            
    if best_match:
        return best_match[0], best_match[1], next_search_start
    else:
        return None, None, None

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
                refined_output += f"{line}\n"
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
