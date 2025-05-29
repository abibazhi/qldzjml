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
    # 强力清理非JSON内容
    content = re.sub(r'```|json|#.*|\n', '', content)
    content = re.sub(r'\s+', ' ', content)
    content = content.replace("'", '"').strip()
    
    try:
        data = json.loads(content)
        is_match = data.get("is_match", False)
        sutras = data.get("sutras", [])
        if not sutras and "sutra" in data:
            sutras = [{"sutra": data["sutra"], "translator": data.get("translator", "")}]
        recognized_sutras = [item["sutra"] for item in sutras]
        return is_match, sutras, recognized_sutras
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        print(f"原始内容: {content}")
        is_match = "is_match\": true" in content
        pattern = r'"sutra":"([^"]+)", *"translator":"([^"]+)"'
        matches = re.findall(pattern, content)
        sutras = [{"sutra": s, "translator": t} for s, t in matches]
        recognized_sutras = [s for s, t in matches]
        return is_match, sutras, recognized_sutras

def load_progress(progress_file):
    if not os.path.exists(progress_file):
        return set()
    with open(progress_file, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f)

def save_progress(progress_file, book_id):
    with open(progress_file, 'a', encoding='utf-8') as f:
        f.write(f"{book_id}\n")

def main():
    #books = [{"id": "020/259", "path": "020/259", "name": "佛说须摩提菩萨经"}]  # 示例数据
    with open("books.json", "r", encoding="utf-8") as f:
        books = json.load(f)
    print(f"加载数据：{len(books)}条记录")  # 添加此行检查

    progress_file = "progress.log"
    processed_ids = load_progress(progress_file)
    results = []

    for book in books:
        if book['id'] in processed_ids:
            continue
        image_url = f"https://daxumi.cn/qldzj/{book['path']}.png"
        print(f"正在检查：{book['name']} -> {image_url}")
        try:
            message = check_text_in_image(image_url, book['name'])
            is_match, details, recognized_sutras = check_response_content(message)
            print(f"结果：{is_match}")
            print(f"识别详情：{json.dumps(details, ensure_ascii=False, indent=2)}\n")
            results.append({
                "id": book["id"],
                "name": book["name"],
                "match": is_match,
                "recognized_sutras": recognized_sutras,
                "details": details
            })
            save_progress(progress_file, book['id'])
        except Exception as e:
            print(f"发生错误：{e}\n")
            results.append({
                "id": book["id"],
                "name": book["name"],
                "match": "error",
                "error": str(e)
            })

    with open("check_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
