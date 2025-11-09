import os
import json
import time
from pathlib import Path
import unittest
from zhipuai import ZhipuAI
from typing import Dict, List
from openai import OpenAI



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
            api_key=os.environ.get('DEEPSEEK_API_KEY'),
            #api_key='sk-570772014b0447efbfc9b1f577d7d86b',
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

# ======================
# 配置参数
# ======================
BASE_DIR_URL = "https://daxumi.cn/qldzj/"  # 基础URL前缀
EXTENSION = ".png"
QUESTION = "请识别图片中所有文字并打印出来"

# 进度和结果保存路径
PROGRESS_DIR = Path("progress")
OUTPUT_DIR = Path("results")

# 创建目录
PROGRESS_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# 加载最大编号映射
with open("0.2.1.max_png_numbers.json", "r", encoding="utf-8") as f:
    MAX_PAGES = json.load(f)


'''
# ======================
# API 调用函数（请确保 client 和 MODEL 已定义）
# ======================
def analyze_image(image_url: str, question: str) -> str:
    try:
        response = client.chat.completions.create(
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
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"API Error for {image_url}: {e}")
        return None
'''

# ======================
# 进度管理函数
# ======================
def load_progress(subdir: str):
    progress_file = PROGRESS_DIR / f"progress_{subdir}.json"
    try:
        with open(progress_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("last_processed_page", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0

def save_progress(subdir: str, last_page: int):
    progress_file = PROGRESS_DIR / f"progress_{subdir}.json"
    with open(progress_file, 'w', encoding='utf-8') as f:
        json.dump({"last_processed_page": last_page}, f, ensure_ascii=False, indent=4)

# ======================
# 主处理逻辑
# ======================
def process_subdir(subdir: str):
    print(f"\n=== 开始处理子目录 {subdir} ===")
    base_image_url = f"{BASE_DIR_URL}{subdir}/"
    max_page = MAX_PAGES.get(subdir)

    if max_page is None:
        print(f"警告：未在 max_png_numbers.json 中找到 {subdir} 的最大页码，跳过。")
        return

    # 加载进度
    start_page = load_progress(subdir) + 1
    results = []

    # 如果已有部分结果，加载它们
    output_file = OUTPUT_DIR / f"results_{subdir}.json"
    if start_page > 1 and output_file.exists():
        with open(output_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
        print(f"已加载 {len(results)} 条历史结果，从第 {start_page} 页继续...")

    # 开始处理图片
    for page in range(start_page, max_page + 1):
        image_url = f"{base_image_url}{page}{EXTENSION}"
        print(f"[{subdir}] Processing page {page}/{max_page} ...")

        retry_count = 0
        while retry_count < 3:  # 最多重试3次
            result = analyze_image(image_url, QUESTION)
            if result is not None:
                break
            retry_count += 1
            print(f"  重试第 {retry_count} 次...")
            time.sleep(5)

        if result is None:
            print(f"❌ 处理失败，跳过: {image_url}")
            continue  # 可选择记录失败页

        # 成功识别，保存结果
        results.append({"页面": page, "res": result})
        save_progress(subdir, page)  # 更新进度

        # 实时保存到文件（防止中途崩溃）
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)

        print(f"✅ 页面 {page} 处理完成")

    print(f"✅ 子目录 {subdir} 处理完成，共 {len(results)} 页已保存。")

# ======================
# 主程序入口
# ======================
if __name__ == "__main__":
    # 按顺序处理 001 到 168
    for i in range(2, 169):
        subdir = f"{i:03d}"
        if subdir not in MAX_PAGES:
            print(f"跳过未定义的子目录: {subdir}")
            continue
        try:
            process_subdir(subdir)
        except KeyboardInterrupt:
            print(f"\n\n用户中断，程序退出。下次将从最后进度继续。")
            break
        except Exception as e:
            print(f"处理子目录 {subdir} 时发生未知错误: {e}")
            continue  # 继续下一个目录

    print("\n🎉 所有子目录处理完成！")
