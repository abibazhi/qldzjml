###
import pandas as pd
import json
import numpy as np

# 1. 加载 JSON 数据
with open('2.0.3.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# 2. 加载 Excel 文件（假设工作表名是 Sheet1，C列是译者）
excel_df = pd.read_excel("translator.1.大模型验证结果.核对.再加经名.xlsx", sheet_name=0, header=None)
# 假设 A列是第0列，C列是第2列
excel_data = excel_df.iloc[:, [0, 2]].values.tolist()  # 提取 A列和 C列

# 3. 构建一个列表，记录每个编号出现的次数（用于处理重复 id）
counter = {}
result_list = []

# 4. 遍历 JSON 数据
for item in json_data:
    current_id = item["id"]

    # 如果是第一个元素（标题行），直接添加 translator 字段
    if current_id == "编号":
        item["translator"] = "译者"
        result_list.append(item)
        continue

    # 对于其他数据项
    count = counter.get(current_id, 0)

    # 在 Excel 数据中查找第 count 次出现的该 id 对应的译者
    matched = False
    for row in excel_data:
        excel_id = str(row[0])
        if str(current_id) == excel_id:
            if count == 0:
                translator = row[1]
                # 确保译者不是 NaN 或空值
                if isinstance(translator, float) and np.isnan(translator):
                    translator = None
                elif pd.isna(translator):
                    translator = None
                item["translator"] = translator
                result_list.append(item)
                counter[current_id] = counter.get(current_id, 0) + 1
                matched = True
                break
            else:
                count -= 1
        elif pd.isna(row[0]):
            continue  # 忽略空行

    if not matched:
        item["translator"] = None  # 设置为 null 表示没有找到译者
        result_list.append(item)
        print(f"未找到 ID {current_id} 的译者")

# 5. 保存更新后的 JSON
with open('updated_json_file.json', 'w', encoding='utf-8') as f:
    json.dump(result_list, f, ensure_ascii=False, indent=2)

print("✅ 已完成译者字段补充")
