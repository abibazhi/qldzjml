def filter_output(input_file, output_file, max_block_count=12):
    """
    从已有的output.txt中过滤掉文本块数量大于指定值的行，并将结果保存到另一个文件。
    
    :param input_file: 输入文件路径（即原始的output.txt）
    :param output_file: 输出文件路径（过滤后的文件）
    :param max_block_count: 最大文本块数量，超过此数量的行会被过滤掉
    """
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            parts = line.strip().split()
            if len(parts) < 2:  # 确保至少有两个元素：文件名和文本块数
                continue
            try:
                block_count = int(parts[1])
                if block_count <= max_block_count:
                    outfile.write(line)
            except ValueError:
                # 如果无法转换为整数，则跳过该行
                print(f"无法解析文本块数量: {line}")
                continue

if __name__ == "__main__":
    input_txt = 'output.txt'  # 已经识别好的输出文件路径
    filtered_output_txt = 'filtered_output.txt'  # 过滤后的输出文件路径
    
    filter_output(input_txt, filtered_output_txt)
    print("过滤完成，结果已保存至:", filtered_output_txt)
