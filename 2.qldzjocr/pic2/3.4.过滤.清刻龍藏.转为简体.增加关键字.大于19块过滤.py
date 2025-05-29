import opencc

def filter_and_convert(input_file, filtered_output_file, removed_lines_file):
    """
    从已有的output.txt中过滤掉包含特定关键字的行，并且过滤掉文本块总数大于等于19的行。
    将剩下的文本转换为简体汉字后保存到filtered_output_file，同时将被过滤掉的行保存到removed_lines_file。
    
    :param input_file: 输入文件路径（即原始的output.txt）
    :param filtered_output_file: 过滤并转换后的输出文件路径
    :param removed_lines_file: 被过滤掉的行保存的文件路径
    """
    cc = opencc.OpenCC('t2s')  # 使用繁体到简体的转换配置
    
    # 定义需要过滤的关键字列表（包括繁体和简体形式）
    #keywords = ["清刻施藏", "清刻龍藏", "清刻龙藏", "清刺龍藏", "清刺龙藏"]
    keywords = ["清刻施藏", "清刻龍藏", "清刻龙藏", "清刺龍藏", "清刺龙藏","清刻能藏","清刻麓藏","清刻龙葳"] 
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(filtered_output_file, 'w', encoding='utf-8') as filtered_outfile, \
         open(removed_lines_file, 'w', encoding='utf-8') as removed_outfile:
        for line in infile:
            parts = line.strip().split(maxsplit=2)  # 只分割前两部分，保留文本部分不被分割
            if len(parts) < 3:  # 确保至少有三个部分：文件名、文本块数和文本内容
                continue
            filename, block_count_str, text = parts
            
            try:
                block_count = int(block_count_str)
            except ValueError:
                print(f"无法解析文本块数量: {line}")
                continue
            
            # 将文本转换为简体汉字以便统一处理
            converted_text = cc.convert(text)
            
            # 检查文本是否包含任何关键字或文本块数量是否大于等于19
            if any(keyword in converted_text for keyword in keywords) or block_count >= 19:
                removed_outfile.write(line)  # 写入被过滤掉的行
                continue  # 跳过包含这些关键字或文本块数量过多的行
            
            # 写入输出文件
            filtered_outfile.write(f"{filename} {block_count_str} {converted_text}\n")

if __name__ == "__main__":
    input_txt = 'output.txt'  # 已经识别好的输出文件路径
    filtered_output_txt = 'filtered_converted_output.txt'  # 过滤并转换后的输出文件路径
    removed_lines_txt = 'removed_lines.txt'  # 被过滤掉的行保存的文件路径
    
    filter_and_convert(input_txt, filtered_output_txt, removed_lines_txt)
    print("过滤并转换完成，结果已保存至:", filtered_output_txt)
    print("被过滤掉的行已保存至:", removed_lines_txt)
