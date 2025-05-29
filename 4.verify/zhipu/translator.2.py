import pandas as pd
import json
from zhconv import convert

# 工具函数：将字符串统一为简体中文用于比较
def normalize(text):
    return convert(text, 'zh-cn')

# 读取Excel数据
excel_path = 'translator.0.编号.图片.经名.译者.xlsx'  # 替换为你自己的路径
df_excel = pd.read_excel(excel_path, engine='openpyxl')

# 确保“编号”列存在，并转为整数类型
if '编号' not in df_excel.columns:
    raise ValueError("Excel中没有找到'编号'列")
df_excel['编号'] = df_excel['编号'].astype(int)

# 构建一个字典：编号 -> 手工核对译者
excel_dict = {}
for _, row in df_excel.iterrows():
    sutra_id = int(row['编号'])
    translator = str(row.get('手工核对译者', '') or '')
    excel_dict[sutra_id] = translator.strip()

# 读取JSONL文件
jsonl_path = 'raw_results.jsonl'  # 替换为你自己的路径
jsonl_dict = {}

with open(jsonl_path, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line.strip())
        sutra_id = int(data.get('id', -1))
        raw_response = data.get('raw_response', '')

        # 提取JSON字符串中的translator字段
        try:
            start_idx = raw_response.index('{')
            end_idx = raw_response.rindex('}')
            json_str = raw_response[start_idx:end_idx + 1]
            parsed = json.loads(json_str)
            translator = parsed.get('translator', '')
        except (ValueError, json.JSONDecodeError) as e:
            translator = ''

        jsonl_dict[sutra_id] = translator.strip()

# 对比两组数据
for sutra_id in sorted(set(excel_dict.keys()) & set(jsonl_dict.keys())):
    excel_translator = normalize(excel_dict[sutra_id])
    json_translator = normalize(jsonl_dict[sutra_id])

    if excel_translator != json_translator:
        print(f"[编号: {sutra_id}] 不一致:")
        print(f"  Excel译者: {excel_dict[sutra_id]}")
        print(f"  JSON译者: {jsonl_dict[sutra_id]}")
        print("-" * 60)
