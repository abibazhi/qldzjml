import pandas as pd
import re

# 输入输出文件路径
input_file = '1.4.extracted_data.手工校对完毕.xlsx'
output_html = 'output.html'

# 读取Excel，不假设有表头，并手动命名列
df = pd.read_excel(input_file, sheet_name=2, header=None)
df.columns = ['编号', '图片文件名', '经文名称']

# 辅助函数：提取清理后的内容
def get_clean_text(text):
    # 第一步：获取第一个逗号之前的内容
    match = re.match(r'^[^,，]+', text)
    if match:
        text = match.group(0).strip()

    # 第二步：去掉括号及其后面的内容
    text = re.split(r'[（\(]', text)[0].strip()

    return text

# 构建表格HTML（仅显示前两列）
html_table = '<table border="1" class="dataframe">\n'

# 手动添加表头（仅显示前两列）
html_table += """  <thead>
    <tr>
      <th style="text-align: left;">编号</th>
      <th style="text-align: left;">链接</th>
    </tr>
  </thead>
  <tbody>
"""

# 遍历每一行并处理
for _, row in df.iterrows():
    col1 = str(row['编号'])        # 第一列：编号
    col2 = str(row['图片文件名'])   # 第二列：图片文件名
    col3 = str(row['经文名称'])     # 第三列：经文名称

    # 提取并清理文字
    display_text = get_clean_text(col3)

    # 使用正则提取编号，并格式化路径
    match = re.match(r"qldzjpng_(\d+)_(\d+)\.png", col2)
    if match:
        processed_col2 = f"qldzj/{match.group(1)}/{match.group(2)}"
    else:
        processed_col2 = "#"

    # 使用清理后的文字作为<a>标签的显示内容
    link_tag = f'<a href="{processed_col2}">{display_text}</a>'

    html_table += f"""    <tr>
      <td>{col1}</td>
      <td>{link_tag}</td>
    </tr>
"""

html_table += "  </tbody>\n</table>"

# 完整HTML结构 + 美化样式
full_html = f"""<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>乾隆大藏经目录</title>
    <style>
        body {{
            font-family: "Microsoft YaHei", sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f9f9f9;
        }}
        h1 {{
            text-align: center;
            font-size: 2em;
            margin-bottom: 30px;
            color: #333;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 0 20px;
            background-color: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
        }}
        th, td {{
            border: 1px solid #999;
            padding: 10px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        a {{
            color: #0066cc;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <h1>乾隆大藏经目录</h1>
    <div class="container">
{html_table}
    </div>
</body>
</html>
"""

# 写入文件
with open(output_html, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f"✅ HTML文件已成功生成: {output_html}")
