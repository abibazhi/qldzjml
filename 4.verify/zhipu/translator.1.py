import pandas as pd
import json

# 读取Excel文件
file_path = 'translator.0.编号.图片.经名.译者.xlsx'  # 将这里的文件路径替换为你的实际文件路径
df = pd.read_excel(file_path, engine='openpyxl')

# 确保编号列存在
if '编号' not in df.columns:
    raise ValueError("Excel文件中没有找到'编号'列")

# 过滤掉没有编号的行
df.dropna(subset=['编号'], inplace=True)

# 强制将编号列转为整数类型（忽略小数部分）
df['编号'] = df['编号'].astype(int)

# 转换成字典列表，准备输出到JSONL
records = df.to_dict(orient='records')

# 输出到JSONL文件
output_file_path = 'output.jsonl'
with open(output_file_path, 'w', encoding='utf-8') as f:
    for record in records:
        f.write(f"{json.dumps(record, ensure_ascii=False)}\n")

print(f"数据已成功保存到{output_file_path}")
