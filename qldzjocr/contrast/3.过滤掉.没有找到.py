def filter_no_match_lines(input_path, output_path):
    """从输入文件中过滤掉包含“没有找到”的行，并将结果写入输出文件"""
    with open(input_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            if "没有找到" not in line:
                outfile.write(line)

# 设置文件路径
input_path = './comparison_result.txt'
output_path = './filtered_comparison_result.txt'  # 过滤后的文件保存位置

filter_no_match_lines(input_path, output_path)
print(f"Filtered TXT output has been saved to {output_path}")
