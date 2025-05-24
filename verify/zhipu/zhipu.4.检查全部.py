import json
from zhipuai import ZhipuAI

# 假设这是你封装好的函数
def check_text_in_image(image_url, sutra_name):
    client = ZhipuAI(api_key="1404e31679389d3b24f6b9a3fa469157.ZXIFA6ijxoyUpg3Y")  # 替换为你的API Key
    response = client.chat.completions.create(
        model="glm-4v-flash",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"请比较图中的经名是否是'{sutra_name}'？如果是，回答请以'是的'开始；如果不是请以'不是'开始"},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ]
    )
    return response.choices[0].message

# 解析响应内容返回布尔值
def check_response_content(message):
    if message.content.startswith("是的"):
        return True
    elif message.content.startswith("不是"):
        return False
    else:
        raise ValueError(f"未知响应内容: {message.content}")

# 主程序逻辑
def main():
    # 加载 books.json 文件
    with open("books.json", "r", encoding="utf-8") as f:
        books = json.load(f)

    results = []

    for book in books:
        path = book["path"]
        name = book["name"]

        # 构造图片URL
        image_url = f"https://daxumi.cn/qldzj/{path}.png"

        print(f"正在检查：{name} -> {image_url}")

        try:
            message = check_text_in_image(image_url, name)
            is_match = check_response_content(message)
            print(f"结果：{is_match}\n")
            results.append({
                "id": book["id"],
                "name": name,
                "match": is_match
            })
        except Exception as e:
            print(f"发生错误：{e}\n")
            results.append({
                "id": book["id"],
                "name": name,
                "match": "error",
                "error": str(e)
            })

    # 可选：保存结果到文件
    with open("check_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
