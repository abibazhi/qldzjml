import json
import os
import re
from zhipuai import ZhipuAI

def check_text_in_image(image_url, sutra_name):
    client = ZhipuAI(api_key="1404e31679389d3b24f6b9a3fa469157.ZXIFA6ijxoyUpg3Y")
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
    
    # 移除所有反引号（```json 和 ```）
    content = re.sub(r'```json?', '', content, flags=re.IGNORECASE)
    
    # 移除可能的行号和前缀
    content = re.sub(r'^\d+\.\s*', '', content.strip())
    
    # 规范化JSON格式
    content = content.replace("'", '"')  # 单引号转双引号
    content = re.sub(r'(\w+):', r'"\1":', content)  # 为未加引号的键添加引号
    
    try:
        # 解析JSON
        data = json.loads(content)
        
        # 处理单条记录的情况（非数组）
        is_match = data.get("is_match", False)
        sutras = data.get("sutras", [])
        if not sutras and "sutra" in data:  # 兼容旧格式（单条记录非数组）
            sutras = [{"sutra": data["sutra"], "translator": data.get("translator", "")}]
        
        # 提取识别出的经名
        recognized_sutras = [item.get("sutra", "") for item in sutras]
        
        return is_match, sutras, recognized_sutras
    
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        print(f"原始内容: {content}")
        
        # 备用方案：从非标准格式中提取
        is_match = False
        sutras = []
        recognized_sutras = []
        
        # 先尝试提取is_match
        if "is_match" in content:
            is_match = "true" in content.lower()
        
        # 提取经名和译者（兼容单条或多条）
        pattern = r'"sutra":"([^"]+)","translator":"([^"]+)"'
        matches = re.findall(pattern, content)
        for match in matches:
            sutras.append({"sutra": match[0], "translator": match[1]})
            recognized_sutras.append(match[0])
        
        return is_match, sutras, recognized_sutras

# 其他函数（load_progress、save_progress、main）保持不变，见上文
def load_progress(progress_file):
    """加载进度"""
    if not os.path.exists(progress_file):
        return set()
    with open(progress_file, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f)

def save_progress(progress_file, book_id):
    """保存进度"""
    with open(progress_file, 'a', encoding='utf-8') as f:
        f.write(f"{book_id}\n")

def main():
    # 加载 books.json 文件
    with open("books.json", "r", encoding="utf-8") as f:
        books = json.load(f)

    # 加载进度
    progress_file = "progress.log"
    processed_ids = load_progress(progress_file)

    results = []
    if os.path.exists("check_results.json"):
        with open("check_results.json", "r", encoding="utf-8") as f:
            results = json.load(f)

    processed_count = len(processed_ids)
    for idx, book in enumerate(books):
        if book['id'] in processed_ids:
            continue

        path = book["path"]
        name = book["name"]

        # 构造图片URL
        image_url = f"https://daxumi.cn/qldzj/{path}.png"

        print(f"正在检查：{name} -> {image_url}")

        try:
            # 调用大模型检查图片
            message = check_text_in_image(image_url, name)
            is_match, details, recognized_sutras = check_response_content(message)

            print(f"结果：{is_match}")
            print(f"识别详情：{json.dumps(details, ensure_ascii=False, indent=2)}\n")

            # 保存当前的结果
            results.append({
                "id": book["id"],
                "name": name,
                "match": is_match,
                "recognized_sutras": recognized_sutras,
                "details": details
            })
            save_progress(progress_file, book["id"])

            # 更新结果文件
            with open("check_results.json", "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"发生错误：{e}\n")
            results.append({
                "id": book["id"],
                "name": name,
                "match": "error",
                "error": str(e)
            })
            # 即使出错也记录进度，防止下次重复尝试
            save_progress(progress_file, book["id"])

if __name__ == "__main__":
    main()
