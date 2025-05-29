from zhipuai import ZhipuAI
client = ZhipuAI(api_key="1404e31679389d3b24f6b9a3fa469157.ZXIFA6ijxoyUpg3Y") # 填写您自己的APIKey
response = client.chat.completions.create(
    model="glm-4v-flash",  # 填写需要调用的模型名称
    messages=[
       {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "请比较图中的经名是否是'大般若波羅蜜多經'？如果是，回答请以'是的'开始；如果不是请以'不是'开始"
          },
          {
            "type": "image_url",
            "image_url": {
                "url" : "https://daxumi.cn/qldzj/038/620.png"
                #"url" : "https://daxumi.cn/qldzj/001/165.png"
            }
          }
        ]
      }
    ]
)
print(response.choices[0].message)
