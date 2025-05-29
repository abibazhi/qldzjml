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

    parsed_lines = []
    for line in lines:
        parts = line.strip().split(': ', 1)
        if len(parts) != 2:
            continue  # 跳过格式不正确的行
        sutra_name, result = parts
        file_path = result.split(' (')[0]  # 提取文件路径部分
        indices = extract_indices(file_path)
        if not indices:
            continue  # 如果无法解析索引，则跳过该行
        parsed_lines.append((sutra_name, result, indices))

    results = []
    overtakes = set()
    
    for i in range(1, len(parsed_lines)):
        current_indices = parsed_lines[i][2]
        previous_indices = parsed_lines[i-1][2]
        if current_indices < previous_indices:
            overtakes.add(i-1)

    # 标记插队项并生成结果
    for i, (sutra_name, result, indices) in enumerate(parsed_lines):
        if i in overtakes:
            results.append(f"{sutra_name}: {result} (插队)")
        else:
            results.append(f"{sutra_name}: {result}")

    # 写入结果到输出文件
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for result in results:
            outfile.write(f"{result}\n")

if __name__ == "__main__":
    input_file = "comparison_result_with_sliding_window_levels.txt"  # 输入文件路径
    output_file = "comparison_result_with_sliding_window_levels_checked.txt"  # 输出文件路径
    
    check_and_mark_overtakes(input_file, output_file)
    print(f"已将检查和标记后的结果保存到 {output_file}")
