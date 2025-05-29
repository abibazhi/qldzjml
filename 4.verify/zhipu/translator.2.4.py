import pandas as pd
import json
import re
from zhconv import convert

# 工具函数：标准化字符串用于比较（去除空格、标点，统一简体）
def normalize(text):
    # 1. 统一为简体中文
    text = convert(text, 'zh-cn')

    # 2. 去除所有空白字符（包括中间的）
    text = re.sub(r'\s+', '', text)

    # 3. 去除所有标点符号（中英文标点都去掉）
    text = re.sub(r'[^\w\u4e00-\u9fa5]', '', text)

    # 4. 手动替换一些特殊字符（如果 zhconv 没有转换到位）
    replacements = {
        '賔': '宾',
        '賓': '宾',
        '曇': '昙',
        '禪': '禅',
        '譯': '译',
        '師': '师',
        '羅': '罗',
        '什': '什',
        '護': '护',
        '蘭': '兰',
        '叉': '叉',
        '又': '叉',   # 如“無羅又” -> “無羅叉”
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    return text

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

                # 如果translator是列表，取第一个元素
                if isinstance(translator, list) and len(translator) > 0:
                    translator = translator[0]
                
                # 确保translator是字符串
                if not isinstance(translator, str):
                    translator = str(translator)

            except (ValueError, json.JSONDecodeError) as e:
                translator = ''

            jsonl_dict[sutra_id] = translator.strip()

    return jsonl_dict

# 比较两个字典中的译者信息
def compare_translators(excel_dict, jsonl_dict):
    for sutra_id in sorted(set(excel_dict.keys()) & set(jsonl_dict.keys())):
        excel_raw = excel_dict[sutra_id]
        json_raw = jsonl_dict[sutra_id]

        excel_norm = normalize(excel_raw)
        json_norm = normalize(json_raw)

        if excel_norm != json_norm:
            print(f"[编号: {sutra_id}] 不一致:")
            print(f"  Excel译者 (原始): {excel_raw}")
            print(f"  JSON译者 (原始): {json_raw}")
            print(f"  Excel译者 (标准化): {excel_norm}")
            print(f"  JSON译者 (标准化): {json_norm}")
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
