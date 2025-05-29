import os

def extract_indices(file_path):
    """从文件路径中提取两个数字索引"""
    base_name = os.path.basename(file_path)
    parts = base_name.split('_')
    if len(parts) >= 3:
        try:
            index1 = int(parts[1])
            index2 = int(parts[2].split('.')[0])
            return (index1, index2)
        except ValueError:
            pass
    return None

def check_and_mark_overtakes(input_file, output_file):
    # 读取输入文件内容
    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    results = []
    last_indices = (-1, -1)

    for line in lines:
        parts = line.strip().split(': ', 1)
        if len(parts) != 2:
            continue  # 跳过格式不正确的行
        sutra_name, result = parts
        file_path = result.split(' (')[0]  # 提取文件路径部分

        current_indices = extract_indices(file_path)
        if not current_indices:
            continue  # 如果无法解析索引，则跳过该行

        if last_indices[0] != -1:
            if current_indices < last_indices:
                result += " (插队)"
            elif current_indices == last_indices:
                # 如果索引相同，也视为插队
                result += " (插队)"

        results.append(f"{sutra_name}: {result}")
        last_indices = current_indices

    # 写入结果到输出文件
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for result in results:
            outfile.write(f"{result}\n")

if __name__ == "__main__":
    input_file = "comparison_result_with_sliding_window_levels.txt"  # 输入文件路径
    output_file = "comparison_result_with_sliding_window_levels_checked.txt"  # 输出文件路径
    
    check_and_mark_overtakes(input_file, output_file)
    print(f"已将检查和标记后的结果保存到 {output_file}")
