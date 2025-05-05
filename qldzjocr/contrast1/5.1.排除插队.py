import os

def check_and_mark_overtakes(input_file, output_file):
    # 读取输入文件内容
    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    results = []
    last_index = -1

    for line in lines:
        parts = line.strip().split(': ', 1)
        if len(parts) != 2:
            continue  # 跳过格式不正确的行
        sutra_name, result = parts
        file_path = result.split(' (')[0]  # 提取文件路径部分

        # 提取文件路径中的数字索引
        try:
            current_index = int(os.path.basename(file_path).split('_')[-1].split('.')[0])
        except ValueError:
            continue  # 如果无法解析索引，则跳过该行

        if last_index != -1 and current_index < last_index:
            results.append(f"{sutra_name}: {result} (插队)")
        else:
            results.append(f"{sutra_name}: {result}")

        last_index = current_index

    # 写入结果到输出文件
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for result in results:
            outfile.write(f"{result}\n")

if __name__ == "__main__":
    input_file = "comparison_result_with_sliding_window_levels.txt"  # 输入文件路径
    output_file = "comparison_result_with_sliding_window_levels_checked.txt"  # 输出文件路径
    
    check_and_mark_overtakes(input_file, output_file)
    print(f"已将检查和标记后的结果保存到 {output_file}")
