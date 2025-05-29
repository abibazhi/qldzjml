def extract_filenames_from_file(filepath):
    filenames = set()
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            # 根据您的格式，提取图片路径中的文件名部分
            if "图片路径" in line:
                filename = line.split(',')[0].split('/')[-1].replace(' ', '')
                filenames.add(filename)
            else:
                # 提取非图片路径格式的行中的文件名
                parts = line.strip().split()
                if len(parts) > 0:
                    filenames.add(parts[0])
    return filenames

def compare_files(file1, file2, output1, output2):
    filenames1 = extract_filenames_from_file(file1)
    filenames2 = extract_filenames_from_file(file2)

    diff1 = filenames1 - filenames2  # 在file1中但不在file2中的文件名
    diff2 = filenames2 - filenames1  # 在file2中但不在file1中的文件名

    with open(output1, 'w', encoding='utf-8') as outfile1, \
         open(output2, 'w', encoding='utf-8') as outfile2:
        outfile1.write('\n'.join(diff1))
        outfile2.write('\n'.join(diff2))

if __name__ == "__main__":
    detected_texts_output = 'detected_texts_output.txt'
    filtered_converted_output = 'filtered_converted_output.txt'
    output_diff1 = 'diff_in_detected_not_in_filtered.txt'
    output_diff2 = 'diff_in_filtered_not_in_detected.txt'

    compare_files(detected_texts_output, filtered_converted_output, output_diff1, output_diff2)
    print(f"差异结果已保存至: {output_diff1} 和 {output_diff2}")
