import pandas as pd
import re

input_file = '1.4.extracted_data.手工校对完毕.xlsx'
output_html = 'output.html'

df = pd.read_excel(input_file, sheet_name=2)

# 构建表格HTML
html_table = '<table border="1" class="dataframe">\n  <thead>\n    <tr>\n'

# 输出所有表头，并强制左对齐
for col in df.columns:
    html_table += f'      <th style="text-align: left;">{str(col)}</th>\n'
html_table += '    </tr>\n  </thead>\n  <tbody>\n'

# 遍历每一行
for _, row in df.iterrows():
    col1 = str(row.iloc[0])
    col2 = str(row.iloc[1])
    col3 = str(row.iloc[2])

    match = re.match(r"qldzjpng_(\d+)_(\d+)\.png", col2)
    if match:
        processed_col2 = f"qldzj/{match.group(1)}/{match.group(2)}"
    else:
        processed_col2 = "#"

    link_tag = f'<a href="{processed_col2}">{col3}</a>'

    html_table += f"""    <tr>
      <td>{col1}</td>
      <td>{link_tag}</td>
      <td>{col3}</td>
    </tr>
"""

html_table += '  </tbody>\n</table>'

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
