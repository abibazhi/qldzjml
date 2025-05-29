from opencc import OpenCC

# 初始化OpenCC，配置为繁体转简体
cc = OpenCC('t2s')

def convert_to_simplified(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    converted_lines = []
    for line in lines:
        # 将每行中的繁体字转换为简体字
        converted_line = cc.convert(line)
        converted_lines.append(converted_line)

    # 写入新的文件
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for converted_line in converted_lines:
            outfile.write(converted_line)

if __name__ == "__main__":
    input_file_path = "detected_texts_output.txt"  # 输入文件路径
    output_file_path = "detected_texts_output_simplified.txt"  # 输出文件路径
    
    convert_to_simplified(input_file_path, output_file_path)
    print(f"已将繁体字转换为简体字并保存到 {output_file_path}")
