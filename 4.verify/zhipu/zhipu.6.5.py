import json
import os
import re
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
    return response.choices[0].message


def check_response_content(message):
    content = message.content
    content = re.sub(r'```json?', '', content, flags=re.IGNORECASE)  # 移除代码块标记
    content = re.sub(r'^\d+\.\s*', '', content.strip())  # 移除行号
    content = content.replace("'", '"').replace('\n', ' ')  # 规范化格式
    try:
        data = json.loads(content)
        is_match = data.get("is_match", False)
        sutras = data.get("sutras", [])
        if not sutras and "sutra" in data:  # 兼容单条记录
            sutras = [{"sutra": data["sutra"], "translator": data.get("translator", "")}]
        recognized_sutra = sutras[0]["sutra"] if sutras else ""
        return is_match, recognized_sutra
    except Exception as e:
        print(f"解析错误: {e}，原始内容: {content}")
        return False, ""


def load_progress(progress_file):
    return set(line.strip() for line in open(progress_file, 'r', encoding='utf-8')) if os.path.exists(progress_file) else set()


def save_progress(progress_file, book_id):
    with open(progress_file, 'a', encoding='utf-8') as f:
        f.write(f"{book_id}\n")


def main():
    progress_file = "progress.log"
    output_file = "formatted_results.json"
    books = json.load(open("books.json", "r", encoding="utf-8"))  # 输入文件（经名列表）
    processed = load_progress(progress_file)
    results = []

    for book in books:
        if book['id'] in processed:
            continue
        try:
            image_url = f"https://daxumi.cn/qldzj/{book['path']}.png"
            print(f"处理: {book['name']} -> {image_url}")
            message = check_text_in_image(image_url, book['name'])
            is_match, recognized_sutra = check_response_content(message)
            
            # 构造目标格式
            result = {
                "id": book["id"],
                "originname": book["name"],
                "recognized_sutra": recognized_sutra,
                "match": is_match
            }
            results.append(result)
            save_progress(progress_file, book['id'])
            print(f"结果: {result}\n")
            
        except Exception as e:
            print(f"错误: {book['id']} - {str(e)}")
            results.append({
                "id": book["id"],
                "originname": book["name"],
                "recognized_sutra": "",
                "match": "error",
                "error": str(e)
            })

    # 保存最终结果
    json.dump(results, open(output_file, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"结果已保存至 {output_file}")


if __name__ == "__main__":
    main()
