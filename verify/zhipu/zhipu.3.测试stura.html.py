from zhipuai import ZhipuAI

def check_text_in_image(image_url, sutra_name):
    # 初始化客户端
    client = ZhipuAI(api_key="1404e31679389d3b24f6b9a3fa469157.ZXIFA6ijxoyUpg3Y")  # 填写您自己的APIKey
    
    # 创建请求
    response = client.chat.completions.create(
        model="glm-4v-flash",  # 填写需要调用的模型名称
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"1、请比较图中的经名是否是'{sutra_name}'？如果是，回答请以'是的'开始；如果不是请以'不是'开始。2、打印图中识别出来的经名，如果识别出来繁体字，请不必转化为简体字3、通常，最左侧是经名，中间的文字则是经名加译者名，请把经名和译者名分别打印出来"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    }
                ]
            }
        ]
    )
    
    # 返回响应内容
    return response.choices[0].message

# 示例调用
image_url = "https://daxumi.cn/sutra.html?start=016239&end=016328"
sutra_name = "大般若波羅蜜多經"
result = check_text_in_image(image_url, sutra_name)
print(result)
