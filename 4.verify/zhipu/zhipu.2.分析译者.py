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
                        "text": f"1请识别图片中的佛经的经名及其译者。2、通常，最左侧的小字是经名，中间的大字则是经名，经名的左侧或下面的小字是译者，都是请把经名和译者名分别打印出来。3、用json格式。比如stura:经名,translator:译者。4、识别文字不需要转化为简体。5、可能存在两种及以上经文，都需要描述。5、请检查经名是否存在'{sutra_name}'？如果存在，回答请以'是的'开始；如果不是回答请以'不是'开始。是否存在的回答单独一行，不在json数据中。"
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
image_url = "https://daxumi.cn/qldzj/038/620.png"
sutra_name = "大般若波羅蜜多經"
result = check_text_in_image(image_url, sutra_name)
print(result)
