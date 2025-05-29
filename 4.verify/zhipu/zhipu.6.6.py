import json
import os
from zhipuai import ZhipuAI

def check_text_in_image(image_url, sutra_name):
    client = ZhipuAI(api_key="1404e31679389d3b24f6b9a3fa469157.ZXIFA6ijxoyUpg3Y")  # 替换为有效API密钥
    response = client.chat.completions.create(
        model="glm-4v-flash",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"1. 请检查经名是否存在'{sutra_name}'？\n2. 请识别图片中的佛经的经名sutra及其译者名translator，用json格式包含所有信息。\n3. 识别文字不需要转化为简体。\n4. 可能存在两种及以上经文，都需要描述。\n5. 是否存在的回答放在json数据中，属性名用is_match，值为true或false。"},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ]
    )
    return response.choices[0].message  # 直接返回原始响应内容

def load_progress(progress_file):
    return set(line.strip() for line in open(progress_file, 'r', encoding='utf-8')) if os.path.exists(progress_file) else set()

def save_progress(progress_file, book_id):
    with open(progress_file, 'a', encoding='utf-8') as f:
        f.write(f"{book_id}\n")

def main():
    progress_file = "progress.log"
    output_file = "raw_results.jsonl"  # 逐行保存的JSONL文件
    books = json.load(open("books.json", "r", encoding="utf-8"))
    processed = load_progress(progress_file)
    current_results = []

    # 加载已有结果（支持中断续传）
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            current_results = [json.loads(line) for line in f if line.strip()]

    for book in books:
        if book['id'] in processed:
            continue
        try:
            image_url = f"https://daxumi.cn/qldzj/{book['path']}.png"
            print(f"处理: {book['name']} -> {image_url}")
            raw_response = check_text_in_image(image_url, book['name'])
            print(raw_response)
            
            # 保存原始响应及元数据
            result_entry = {
                "id": book["id"],
                "originname": book["name"],
                "image_url": image_url,
                "raw_response": raw_response,  # 保留原始服务器响应
                "processed_time": datetime.datetime.now().isoformat()  # 可选：记录处理时间
            }
            
            # 追加到JSONL文件（每行一个JSON对象）
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(result_entry, ensure_ascii=False) + "\n")
            
            save_progress(progress_file, book['id'])
            print(f"已保存原始响应: {book['id']}\n")
            
        except Exception as e:
            print(f"错误: {book['id']} - {str(e)}")
            result_entry = {
                "id": book["id"],
                "originname": book["name"],
                "error": str(e),
                "processed_time": datetime.datetime.now().isoformat()
            }
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(result_entry, ensure_ascii=False) + "\n")

    print(f"所有任务处理完成，结果保存至 {output_file}")

if __name__ == "__main__":
    import datetime
    main()
