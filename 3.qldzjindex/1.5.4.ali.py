import pandas as pd
import re

input_file = '1.4.extracted_data.手工校对完毕.xlsx'
output_html = 'output.html'

# 读取Excel，不假设有表头，并手动命名三列
df = pd.read_excel(input_file, sheet_name=2, header=None)
df.columns = ['编号', '图片文件名', '经文名称']  # 必须保留全部三列

# 构建表格HTML（只显示前两列）
html_table = '<table border="1" class="dataframe">\n'

# 手动添加表头（仅显示前两列）
html_table += """  <thead>
    <tr>
      <th style="text-align: left;">编号</th>
      <th style="text-align: left;">图片文件名</th>
    </tr>
  </thead>
  <tbody>
"""

# 遍历每一行并处理
for _, row in df.iterrows():
    col1 = str(row['编号'])        # 第一列：编号
    col2 = str(row['图片文件名'])   # 第二列：图片文件名

    # 使用正则提取编号，并格式化路径
    match = re.match(r"qldzjpng_(\d+)_(\d+)\.png", col2)
    if match:
        processed_col2 = f"qldzj/{match.group(1)}/{match.group(2)}"
    else:
        processed_col2 = "#"

    link_tag = f'<a href="{processed_col2}">{processed_col2}</a>'

    html_table += f"""    <tr>
      <td>{col1}</td>
      <td>{link_tag}</td>
    </tr>
"""

html_table += "  </tbody>\n</table>"

# 完整HTML结构
full_html = f"""<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>Excel 转 HTML</title>
    <style>
        table {{
            border-collapse: collapse;
            width: 100%;
        }}
        th, td {{
            border: 1px solid #999;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        a {{
            color: blue;
            text-decoration: underline;
        }}
    </style>
</head>
<body>
{html_table}
</body>
</html>
"""

# 写入文件
with open(output_html, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f"✅ HTML文件已成功生成: {output_html}")
