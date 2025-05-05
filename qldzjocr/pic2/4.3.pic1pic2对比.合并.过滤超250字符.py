def filter_lines_by_length(input_filename, output_filename, max_length=250):
    """
    过滤文件中的行，保留长度不超过指定字符数的行。
    
    :param input_filename: 输入文件名
    :param output_filename: 输出文件名
    :param max_length: 每行的最大允许字符数
    """
    filtered_lines = []
    with open(input_filename, 'r', encoding='utf-8') as file:
        for line in file:
            if len(line) <= max_length:
                filtered_lines.append(line)

    # 将过滤后的行写入输出文件
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        outfile.writelines(filtered_lines)

if __name__ == "__main__":
    input_filename = 'cleaned_merged_output.txt'
    output_filename = 'filtered_cleaned_merged_output.txt'

    filter_lines_by_length(input_filename, output_filename)
