from bs4 import BeautifulSoup
import argparse

def remove_nan_rows(input_file, output_file):
    # 读取输入 HTML 文件
    with open(input_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 解析 HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 查找所有 tr 行
    for row in soup.find_all('tr'):
        # 检查这一行是否包含文本为 'nan' 的单元格
        if any(cell.get_text(strip=True) == 'nan' for cell in row.find_all('td')):
            row.decompose()  # 删除该行

    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    print(f"处理完成，已写入文件：{output_file}")

# 命令行参数解析
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='从HTML表格中删除包含 "nan" 的行')
    parser.add_argument('input', help='2.0.4.html')
    parser.add_argument('output', help='2.0.4.1.html')

    args = parser.parse_args()
    remove_nan_rows(args.input, args.output)
