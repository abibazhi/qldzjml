import opencc

def filter_and_convert(input_file, output_file):
    """
    从已有的output.txt中过滤掉以"清刻龍藏"开头的行，并将剩下的文本转换为简体汉字后保存到另一个文件。
    
    :param input_file: 输入文件路径（即原始的output.txt）
    :param output_file: 输出文件路径（过滤并转换后的文件）
    """
    cc = opencc.OpenCC('t2s')  # 使用繁体到简体的转换配置
    
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            parts = line.strip().split()
            if len(parts) < 3:  # 确保至少有三个部分：文件名、文本块数和文本内容
                continue
            text = ' '.join(parts[2:])  # 获取文本部分
            if text.startswith("清刻龍藏"):
                continue  # 跳过以"清刻龍藏"开头的行
            
            # 将文本转换为简体汉字
            converted_text = cc.convert(text)
            
            # 重新组合行并写入输出文件
            outfile.write(f"{parts[0]} {parts[1]} {converted_text}\n")

if __name__ == "__main__":
    input_txt = 'output.txt'  # 已经识别好的输出文件路径
    filtered_output_txt = 'filtered_converted_output.txt'  # 过滤并转换后的输出文件路径
    
    filter_and_convert(input_txt, filtered_output_txt)
    print("过滤并转换完成，结果已保存至:", filtered_output_txt)
