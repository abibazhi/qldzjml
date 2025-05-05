import base64

def convert_result_to_html(result_file, html_output_file):
    # 读取结果文件内容
    with open(result_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 准备HTML输出
    html_content = "<html><body><table border='1'><tr><th>图片路径</th><th>文本</th><th>匹配到的标准文本</th><th>匹配到的行号</th></tr>"
    
    for line in lines:
        line = line.strip()
        parts = line.split(", ", 1)
        img_path = parts[0]
        text_block = parts[1].split("(匹配到的标准文本: ")[0].strip()
        
        if "(匹配到的标准文本:" in line:
            match_info = line.split("(匹配到的标准文本: ")[1]
            standard_text = match_info.split(" (行号: ")[0].replace("\"", "")
            line_number = match_info.split(" (行号: ")[1].split(")")[0]

            html_content += f"<tr><td>{img_path}</td><td>{text_block}</td><td>{standard_text}</td><td>{line_number}</td></tr>"
        else:
            # 如果没有匹配信息，则只显示文本块和图片路径
            html_content += f"<tr><td>{img_path}</td><td>{text_block}</td><td>-</td><td>-</td></tr>"

    html_content += "</table></body></html>"

    # 写入HTML文件
    with open(html_output_file, 'w', encoding='utf-8') as file:
        file.write(html_content)

    print(f"已将比较结果转换为HTML并保存到 {html_output_file}")

if __name__ == "__main__":
    result_file = "comparison_result_with_sliding_window_levels.txt"  # 结果文件路径
    html_output_file = "comparison_result_with_sliding_window_levels.html"  # HTML输出文件路径

    convert_result_to_html(result_file, html_output_file)
