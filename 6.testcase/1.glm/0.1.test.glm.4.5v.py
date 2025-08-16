import requests
import json
import time

# =======================
# 配置区
# =======================
API_KEY = "1404e31679389d3b24f6b9a3fa469157.ZXIFA6ijxoyUpg3Y"  # 替换为您的密钥
BASE_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
MODEL = "glm-4.5v"

SUTRA_INFO = {
    "sutraNumber": 212,
    "title": "菩萨睒子经一卷",
    "coverImageUrl": "https://daxumi.cn/qldzj/038/468.png",
    "metadataImageUrl": "https://daxumi.cn/qldzj/038/469.png"
}

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept-Language": "en-US,en"
}

# =======================
# 封装函数：调用 GLM-4.5V 分析图像
# =======================
def analyze_image_with_glm_45v(image_url: str, question: str, stream=False) -> str:
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": image_url}},
                    {"type": "text", "text": question}
                ]
            }
        ],
        "thinking": {"type": "enabled"},  # 显示 AI 思考过程
        "stream": stream
    }

    response = requests.post(BASE_URL, headers=headers, data=json.dumps(payload), stream=stream)

    if stream:
        # 处理流式输出
        result = ""
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8').strip()
                if line_str.startswith("data:"):
                    data = line_str[5:].strip()
                    if data == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data)
                        content = chunk["choices"][0]["delta"].get("content", "")
                        result += content
                        print(content, end="", flush=True)
                    except:
                        continue
        print()  # 换行
        return result
    else:
        # 非流式
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()

# 示例：测试封面是否为“五经同卷”
question = """
请分析这张古籍影印图：
1. 图像中央是否有四个大字？
2. 这四个字是否是“五经同卷”？
3. 页面上是否出现了“菩萨睒子经”或具体经名？
4. 是否有“西晋”、“失译”等译者信息？

回答要求：
- 如果仅为“五经同卷”且无其他经名，请以“是的，符合合卷封面特征”开始。
- 否则以“不是，包含具体信息”开始。
"""

result = analyze_image_with_glm_45v(SUTRA_INFO["coverImageUrl"], question, stream=True)
print("\n【最终回答】", result)
