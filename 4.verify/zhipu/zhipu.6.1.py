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
                    {"type": "text", "text": f"1. 请检查经名是否存在'{sutra_name}'？如果存在，回答请以'是的'开始；如果不是回答请以'不是'开始。\n2. 请识别图片中的佛经的经名及其译者，用json格式，比如sutra:经名,translator:译者。\n3. 识别文字不需要转化为简体。\n4. 可能存在两种及以上经文，都需要描述。\n5. 是否存在的回答单独一行，不在json数据中。"},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ]
    )
    return response.choices[0].message

def check_response_content(message):
    content = message.content
    
    # 提取存在性判断（第一行）
    lines = content.strip().split('\n')
    exists_line = lines[0].strip()
    exists = exists_line.startswith("是的")
    
    # 提取JSON数据（剩余内容）
    json_text = "\n".join(lines[1:]).strip()
    
    # 处理可能的前缀编号和分隔符
    json_text = re.sub(r'^\d+\.\s*', '', json_text)  # 移除行首的"数字. "格式
    
    # 尝试解析JSON
    try:
        # 处理单引号格式
        json_text = json_text.replace("'", '"')
        # 处理不规范的JSON（如:sutra和translator不在双引号中）
        json_text = re.sub(r'(\w+):', r'"\1":', json_text)
        
        # 解析JSON
        details = json.loads(json_text)
        
        # 确保结果是列表格式
        if isinstance(details, dict):
            details = [details]
            
        # 提取识别出的经名
        recognized_sutras = [item["sutra"] for item in details]
        
        return exists, details, recognized_sutras
    
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        print(f"原始内容: {json_text}")
        
        # 尝试使用正则表达式提取
        recognized_sutras = []
        details = []
        
        # 匹配sutra:经名,translator:译者格式
        pattern = r'sutra:([^,]+),translator:([^}]+)'
        matches = re.findall(pattern, json_text)
        
        for match in matches:
            details.append({
                "sutra": match[0].strip(),
                "translator": match[1].strip()
            })
            recognized_sutras.append(match[0].strip())
            
        return exists, details, recognized_sutras

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
