import pandas as pd
import json
from zhconv import convert

# 工具函数：将字符串统一为简体中文用于比较
def normalize(text):
    return convert(text, 'zh-cn')

# 读取Excel数据并处理编号列
def read_excel(file_path):
    df_excel = pd.read_excel(file_path, engine='openpyxl')
    
    # 确保“编号”列存在
    if '编号' not in df_excel.columns:
        raise ValueError("Excel中没有找到'编号'列")
    
    # 更安全地将“编号”列转为整数类型，无法转换的设为 NaN，并过滤掉
    df_excel['编号'] = pd.to_numeric(df_excel['编号'], errors='coerce').fillna(0).astype(int)
    
    # 删除编号为 0 的行（假设编号从1开始）
    df_excel = df_excel[df_excel['编号'] != 0]
    
    # 构建字典：编号 -> 手工核对译者
    excel_dict = {}
    for _, row in df_excel.iterrows():
        sutra_id = int(row['编号'])
        translator = str(row.get('手工核对译者', '') or '')
        excel_dict[sutra_id] = translator.strip()
    
    return excel_dict
'''
# 读取JSONL文件并提取translator字段
def read_jsonl(file_path):
    jsonl_dict = {}

    with open(file_path, 'r', encoding='utf-8') as f:
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

    return jsonl_dict
'''
def read_jsonl(file_path):
    jsonl_dict = {}

    with open(file_path, 'r', encoding='utf-8') as f:
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
                # 确保是字符串类型
                if isinstance(translator, list):
                    translator = ', '.join(translator)  # 如果是列表，转为逗号分隔字符串
                elif not isinstance(translator, str):
                    translator = str(translator)  # 其他类型也转为字符串
            except (ValueError, json.JSONDecodeError) as e:
                translator = ''

            jsonl_dict[sutra_id] = translator.strip()

    return jsonl_dict



# 比较两个字典中的译者信息
def compare_translators(excel_dict, jsonl_dict):
    for sutra_id in sorted(set(excel_dict.keys()) & set(jsonl_dict.keys())):
        excel_translator = normalize(excel_dict[sutra_id])
        json_translator = normalize(jsonl_dict[sutra_id])

        if excel_translator != json_translator:
            print(f"[编号: {sutra_id}] 不一致:")
            print(f"  Excel译者: {excel_dict[sutra_id]}")
            print(f"  JSON译者: {jsonl_dict[sutra_id]}")
            print("-" * 60)



if __name__ == "__main__":
    # 替换为你的实际文件路径
    excel_file_path = 'translator.0.编号.图片.经名.译者.xlsx'
    jsonl_file_path = 'raw_results.jsonl'

    print("开始读取Excel文件...")
    excel_data = read_excel(excel_file_path)
    print(f"Excel中共读取到 {len(excel_data)} 条有效记录")

    print("开始读取JSONL文件...")
    jsonl_data = read_jsonl(jsonl_file_path)
    print(f"JSONL中共读取到 {len(jsonl_data)} 条有效记录")

    common_ids = set(excel_data.keys()) & set(jsonl_data.keys())
    print(f"共有 {len(common_ids)} 个编号在两个文件中都存在")

    if len(common_ids) == 0:
        print("⚠️ 警告：没有共同编号，无法进行比较！请检查文件是否对应")
    else:
        print("开始对比译者字段...")
        compare_translators(excel_data, jsonl_data)
        print("✅ 对比完成")
'''
if __name__ == "__main__":
    # 替换为你的实际文件路径

    excel_file_path = 'your_excel_file.xlsx'
    jsonl_file_path = 'your_jsonl_file.jsonl'
    # 读取Excel和JSONL文件
    excel_data = read_excel(excel_file_path)
    jsonl_data = read_jsonl(jsonl_file_path)

    # 比较译者信息
    compare_translators(excel_data, jsonl_data)
'''
