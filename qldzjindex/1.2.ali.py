import pandas as pd

# 读取Excel文件
input_file = '1.origin.xlsx'
df = pd.read_excel(input_file)

# 提取A, B, F列，并重排序使F列在最前面
df_extracted = df[['行号', '文件名', '核对名字']]

# 移除F列中为空的行
df_cleaned = df_extracted.dropna(subset=['行号'])

# 将结果保存到新的Excel文件中
output_file = '1.extracted_data.xlsx'
df_cleaned.to_excel(output_file, index=False)

print(f"数据已成功提取并保存到 {output_file}")
