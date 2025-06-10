import pandas as pd
from zhipuai import ZhipuAI
import time
import re
import numpy as np

# 初始化客户端
client = ZhipuAI(api_key="1404e31679389d3b24f6b9a3fa469157.ZXIFA6ijxoyUpg3Y")  # 替换为你自己的 API Key

# 构造图片URL函数
def get_image_url(png_filename):
    match = re.search(r'qldzjpng_(\d+)_(\d+)', png_filename)
    if match:
        folder = match.group(1).zfill(3)  # 保证三位数格式
        image_id = match.group(2)
        return f"https://daxumi.cn/qldzj/{folder}/{image_id}.png"
    else:
        raise ValueError(f"无法解析文件名: {png_filename}")

# 使用大模型判断图片中是否包含指定译者，并返回识别出的译者名称
def check_translator_in_image(image_url, target_translator):
    '''
    prompt = (
        "请完成以下任务：\n"
        f"1. 图片中是否存在译者名称 '{target_translator}'？\n"
        "2. 如果存在，请直接回答'是的'，并打印识别出的译者名称。\n"
        "3. 如果不存在，请尝试识别图片中的译者名称，并与目标译者进行对比。\n"
        "4. 判断两个名字是否表示同一个译者（包括别名、异体字、拼写差异等情况）。\n"
        "5. 如果认为是同一个，请回复'是的'；否则回复'否'。\n"
        "6. 不管结果如何，请打印识别出的译者名称。\n"
        "7. 并与目标译者逐字比较，指出哪些字不同，是否为异体字或简繁转换。\n"
        "8. 如果有多个译者，请列出所有可能的候选人。"
    )
    '''
    '''
    prompt = (
        "请完成以下任务：\n"
        f"1. 请先识别图片中的所有文字。\n"
        f"2. 然后查找是否有译者名称 '{target_translator}'？\n"
        "3. 如果存在，请回答'是的'，并打印识别出的译者名称。\n"
        "4. 如果不存在，请列出所有可能的译者候选名称。\n"
        "5. 对每个识别出的译者名称，逐字与目标译者 '{target_translator}' 进行比较。\n"
        "6. 如果有任何一个字不同，请指出差异，并说明是否为异体字或简繁转换。\n"
        "7. 如果两个名字没有任何字相同，则明确回答'否'，并说明原因。\n"
        "8. 不要随意猜测或编造信息。\n"
        "9. 如果不确定，请说明具体原因。\n"
    )
    '''
    '''
    prompt = f"""
        请完成以下任务：
        1. 请先识别图片中的所有文字。
        2. 然后查找是否有译者名称 '{target_translator}'？
        3. 如果存在，请回答'是的'，并打印识别出的译者名称。
        4. 如果不存在，请列出所有可能的译者候选名称。
        5. 对每个识别出的译者名称，逐字与目标译者 '{target_translator}' 进行比较。
        6. 如果有任何一个字不同，请指出差异，并说明是否为异体字或简繁转换。
        7. 如果两个名字没有任何字相同，则明确回答'否'，并说明原因。
        8. 不要随意猜测或编造信息。
        9. 如果不确定，请说明具体原因。
    """
    '''
    prompt = f"""
        请完成以下任务：
        
        1. 请先识别图片中的所有文字。
        2. 然后查找在上述所有文字中，是否有译者名称 '{target_translator}'？
        3. 如果存在，请直接回答“是的”，并进一步给出译者名称在识别出来的所有文字中的第几行？
        4. 如果不存在，请尝试识别图片中的译者，并列出最可能的一个候选名称。
        5. 对比目标译者 '{target_translator}' 和识别出的译者名称，逐字进行比较：
- 如果两个字不同，但属于异体字（如「宾」vs「賓」）、简繁转换（如「昙」vs「曇」）、同义词（如「师」vs「法师」），请说明并认为它们实质上是相同的。
        6. 最终判断是否一致：
           - 如果只有异体字或同义词差异 → 回答“是的”
           - 如果存在多个不相关的字不同 → 回答“否”
        7. 不要随意猜测或编造信息。
        8. 如果不确定，请说明具体原因。
    """

    print(f"\n提问给大模型:\n{prompt}")
    print(f"图片URL: {image_url}\n")

    try:
        response = client.chat.completions.create(
            model="glm-4v-flash",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }
            ]
        )
        result = response.choices[0].message.content.strip()
        print(f"\n大模型的回答:\n{result}\n")
        return result
    except Exception as e:
        print(f"⚠️ 调用大模型失败: {e}")
        time.sleep(2)
        return None

# 从大模型的回答中提取信息：是否一致 + 识别出的译者
def parse_ai_result(ai_response):
    if ai_response is None:
        return {
            '判断': '调用失败',
            '识别译者': '',
            '逐字对比': ''
        }

    is_consistent = '不一致'
    if '是的' in ai_response or '一致' in ai_response:
        is_consistent = '一致'

    # 提取识别出的译者（假设回答中包含“识别出的译者为‘XXX’”）
    recognized_match = re.search(r"识别出的译者(?:为|是)‘([^’]+)’", ai_response)
    recognized_translator = recognized_match.group(1) if recognized_match else ''

    # 提取逐字比较内容（可以更复杂，这里简化为截取相关段落）
    compare_start = ai_response.find("并与目标译者逐字比较")
    compare_text = ai_response[compare_start:] if compare_start != -1 else ''

    return {
        '判断': is_consistent,
        '识别译者': recognized_translator,
        '逐字对比': compare_text.strip()
    }

# 主程序入口
if __name__ == "__main__":
    # 输入输出路径
    input_excel_path = "translator.0.编号.图片.经名.译者.xlsx"
    output_excel_path = "translator.1.大模型验证结果.xlsx"

    # 读取Excel数据
    df = pd.read_excel(input_excel_path)

    # 确保必要的列存在
    required_columns = ['编号', '手工核对译者', '图片']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"缺少必要列: {col}")

    results = []

    # 遍历每一行处理
    for idx, row in df.iterrows():
        sutra_id = row.get('编号', np.nan)

        if pd.isna(sutra_id):
            print(f"[警告] 编号为空，跳过此行")
            continue
    
        sutra_id = int(sutra_id)
        #sutra_id = int(row['编号'])


        translator = str(row.get('手工核对译者', '') or '')
        png_file = str(row.get('图片', '') or '')

        if not translator or not png_file:
            print(f"[跳过] 编号 {sutra_id} 数据不完整")
            continue

        try:
            image_url = get_image_url(png_file)
        except ValueError as ve:
            print(f"[跳过] 编号 {sutra_id}: {ve}")
            continue

        print(f"【正在处理】编号 {sutra_id}，译者：'{translator}'")
        ai_response = check_translator_in_image(image_url, translator)
        parsed_result = parse_ai_result(ai_response)

        results.append({
            '编号': sutra_id,
            '译者（原始）': translator,
            '图片文件名': png_file,
            '图片URL': image_url,
            '大模型回答': ai_response or '',
            '是否一致': parsed_result['判断'],
            '识别出的译者': parsed_result['识别译者'],
            '逐字对比': parsed_result['逐字对比']
        })

        time.sleep(2)  # 控制请求频率，避免触发限流

    # 写入结果到Excel
    result_df = pd.DataFrame(results)
    result_df.to_excel(output_excel_path, index=False, engine='openpyxl')
    print(f"✅ 所有处理完成，结果已保存至: {output_excel_path}")
