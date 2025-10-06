# test_vision_verification.py
import unittest
import json
import time
from zhipuai import ZhipuAI
from typing import Dict, List
from openai import OpenAI

# =======================
# 配置
# =======================
API_KEY = "1404e31679389d3b24f6b9a3fa469157.ZXIFA6ijxoyUpg3Y"  # 替换为您的密钥
MODEL = "glm-4v-flash"
client = ZhipuAI(api_key=API_KEY)

def analyze_image(image_url: str, question: str) -> str:
    try: 
        image_response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": question},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }
            ],
            temperature=0.01
        )
        # 获取图片识别结果
        image_result = image_response.choices[0].message.content.strip()

        print(f"图片识别结果：\n\n{image_result}")
        print("前面50个字符：")
        print(image_result[0:50])
        begin_of_image_result = image_result[0:50]

        # 第二次调用：根据识别结果进行进一步判断
        judge_prompt = "请用json格式输出经名和卷号。没有就输出空"

        clientDeepseek = OpenAI(
            #api_key=os.environ.get('DEEPSEEK_API_KEY'),
            api_key='sk-570772014b0447efbfc9b1f577d7d86b',
            base_url="https://api.deepseek.com")

        judge_response = clientDeepseek.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content":  f"{judge_prompt}\n\n：{begin_of_image_result}"},
            ],
            stream=False
        )
        return judge_response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error processing {image_url}: {e}")
        return None
        
'''
# demo 调用
def analyze_image(image_url: str, question: str) -> str:
    # 这里需要替换为真实的API调用逻辑
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }],
            temperature=0.01
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error processing {image_url}: {e}")
        return None
'''


def load_progress():
    try:
        with open('progress.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"last_processed_page": 0}

def save_progress(last_processed_page):
    with open('progress.json', 'w', encoding='utf-8') as f:
        json.dump({"last_processed_page": last_processed_page}, f)

# 图片的基础URL和扩展名
base_image_url = "https://daxumi.cn/qldzj/001/"
extension = ".png"
question = "请识别图片中所有文字并打印出来"

# 加载已有的进度
progress = load_progress()
start_page = progress["last_processed_page"] + 1

results = []
if start_page > 1:
    with open('output_results.json', 'r', encoding='utf-8') as f:
        results = json.load(f)

for page in range(start_page, 661):
    image_url = f"{base_image_url}{page}{extension}"
    print(f"Processing image {image_url}")
    result = analyze_image(image_url, question)
    if result is not None:
        results.append({"页面": page, "res": result})
        save_progress(page)  # 每次成功处理后保存进度
        with open('output_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
    else:
        print(f"Failed to process {image_url}, will retry.")
        time.sleep(5)  # 简单的错误处理：等待5秒后重试
        page -= 1  # 重试当前页

print("所有图片处理完成，并已保存结果到output_results.json")


'''
imageurl="https://daxumi.cn/qldzj/001/394.png"
question="请识别图片中所有文字并打印出来"  

result = analyze_image(imageurl, question)
print(f"{result}")
'''

