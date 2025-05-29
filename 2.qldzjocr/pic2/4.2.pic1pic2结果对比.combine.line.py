def merge_and_clean_merged_file(merged_filename):
    # 读取原始合并文件内容
    with open(merged_filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 创建字典存储文件名和对应的文本
    file_dict = {}
    for line in lines:
        parts = line.strip().split(' ', 1)
        filename = parts[0]
        text = parts[1] if len(parts) > 1 else ''

        base_name = filename.rstrip('.png')
        if base_name not in file_dict:
            file_dict[base_name] = []

        file_dict[base_name].append(text)

    # 清理并合并文本
    for key in file_dict.keys():
        file_dict[key] = ' '.join(sorted(set(file_dict[key]), key=file_dict[key].index)).strip()

    # 将清理后的数据写回到新的合并文件中
    cleaned_filename = 'cleaned_' + merged_filename
    with open(cleaned_filename, 'w', encoding='utf-8') as outfile:
        for filename in sorted(file_dict.keys()):
            outfile.write(f"{filename}.png {file_dict[filename]}\n")

if __name__ == "__main__":
    merged_filename = 'merged_output.txt'
    merge_and_clean_merged_file(merged_filename)
