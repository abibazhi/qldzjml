import pandas as pd
import re

# 输入文件和输出文件
input_file = '1.4.extracted_data.手工校对完毕.xlsx'
output_html = 'output.html'

# 读取Excel的第三页（索引从0开始，所以是 sheet_name=2）
df = pd.read_excel(input_file, sheet_name=2)

# 创建HTML表格
html_table = '<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n'

# 添加表头，确保所有列名都是字符串
html_table += '      <th>' + '</th><th>'.join(str(col) for col in df.columns) + '</th>\n'
html_table += '    </tr>\n  </thead>\n  <tbody>\n'

# 遍历每一行并处理
for _, row in df.iterrows():
    col1 = str(row.iloc[0])  # 第一列保持不变
    col2 = str(row.iloc[1])  # 第二列处理
    col3 = str(row.iloc[2])  # 第三列用于链接文本

    # 使用正则提取编号，并格式化路径
    match = re.match(r"qldzjpng_(\d+)_(\d+)\.png", col2)
    if match:
        processed_col2 = f"qldzj/{match.group(1)}/{match.group(2)}"
    else:
        processed_col2 = "#"  # 如果不匹配，设为无效链接

    # 构建<a>标签
    link_tag = f'<a href="{processed_col2}">{col3}</a>'

    # 拼接HTML行
    html_table += f'    <tr>\n      <td>{col1}</td>\n      <td>{link_tag}</td>\n      <td>{col3}</td>\n    </tr>\n'

# 结束表格
html_table += '  </tbody>\n</table>'

# 写入HTML文件
with open(output_html, 'w', encoding='utf-8') as f:
    f.write(html_table)

print(f"HTML文件已成功生成: {output_html}")
