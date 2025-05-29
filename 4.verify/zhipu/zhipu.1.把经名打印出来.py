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
                        "text": f"1、请比较图中的经名是否是'{sutra_name}'？如果是，回答请以'是的'开始；如果不是请以'不是'开始。2、并打印图中识别出来的经名，如果识别出来繁体字，请不必转化为简体字。3、请逐一比较识别的经名和问题中给出的经名的每一个字，如果两个字不一样，比如毗和毘这两个字，前者是异体字，所以实质一样，请指出来。4、或者虽然不一样，但是简体和繁体的差别，也请指出。5、识别到的第二个字是毘，但是问题中与之比较的第二个字是毗。如果经名完全一直，请说出为什么这两个字相同的理由？"
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
image_url = "https://daxumi.cn/qldzj/096/153.png"
sutra_name = "阿毘达磨藏显宗论"
result = check_text_in_image(image_url, sutra_name)
print(result)


#image_url = "https://daxumi.cn/qldzj/038/620.png"
#sutra_name = "大般若波羅蜜多經"
