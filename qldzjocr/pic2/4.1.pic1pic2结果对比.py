import os

def extract_filenames_and_texts(filepath):
    filenames = []
    texts = {}
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            if "图片路径" in line:
                filename_with_extension = line.split(',')[0].split('/')[-1].strip()
                filename = os.path.splitext(filename_with_extension)[0]
                text = ','.join(line.split(',')[1:]).strip()
                filenames.append(filename_with_extension)
                texts[filename_with_extension] = text
            else:
                parts = line.strip().split(maxsplit=2)
                if len(parts) > 2:
                    filename_with_extension = f"{parts[0]}.png"
                    text = parts[2]
                    filenames.append(filename_with_extension)
                    texts[filename_with_extension] = text
    return set(filenames), texts

def main(detected_texts_output, filtered_converted_output):
    detected_filenames, detected_texts = extract_filenames_and_texts(detected_texts_output)
    filtered_filenames, filtered_texts = extract_filenames_and_texts(filtered_converted_output)

    diff_detected_not_in_filtered = detected_filenames - filtered_filenames
    diff_filtered_not_in_detected = filtered_filenames - detected_filenames

    # 输出第一种差异情况
    with open('diff_in_detected_not_in_filtered.txt', 'w', encoding='utf-8') as outfile:
        for filename in sorted(diff_detected_not_in_filtered):
            outfile.write(f"{filename} {detected_texts[filename]}\n")

    # 输出第二种差异情况
    with open('diff_in_filtered_not_in_detected.txt', 'w', encoding='utf-8') as outfile:
        for filename in sorted(diff_filtered_not_in_detected):
            outfile.write(f"{filename} {filtered_texts[filename]}\n")

    # 合并信息并输出
    all_filenames = detected_filenames.union(filtered_filenames)
    merged_filename = 'merged_output.txt'
    with open(merged_filename, 'w', encoding='utf-8') as outfile:
        for filename in sorted(all_filenames):
            text = ""
            if filename in detected_texts:
                text += detected_texts[filename] + " "
            if filename in filtered_texts:
                text += filtered_texts[filename] + " "
            outfile.write(f"{filename} {text.strip()}\n")

if __name__ == "__main__":
    detected_texts_output = 'detected_texts_output.txt'
    filtered_converted_output = 'filtered_converted_output.txt'

    main(detected_texts_output, filtered_converted_output)
