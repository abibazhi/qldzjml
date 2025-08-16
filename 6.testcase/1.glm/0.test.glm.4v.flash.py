from zhipuai import ZhipuAI
import unittest
from unittest import TestCase

# =======================
# 配置区
# =======================
API_KEY = "1404e31679389d3b24f6b9a3fa469157.ZXIFA6ijxoyUpg3Y"  # 请替换为您的实际密钥
MODEL = "glm-4-flash-250414"
MODEL = "glm-4.5-flash"
MODEL = "glm-4-flash"
MODEL = "glm-4v-flash"
# MODEL = "glm-4.5v"
SUTRA_INFO = {
    "sutraNumber": 212,
    "title": "菩萨睒子经一卷",
    "catalogIndexPage": "038468",
    "coverImageUrl": "https://daxumi.cn/qldzj/038/468.png",  # 注意：您原图是 620.png，这里按逻辑应为 468.png
    "expectedCoverLabel": "五经同卷",
    "metadataPage": "038469",
    "metadataImageUrl": "https://daxumi.cn/qldzj/038/469.png"
}

client = ZhipuAI(api_key=API_KEY)

# =======================
# 核心函数：调用 GLM-4V 判断图像内容
# =======================
def analyze_image_content(image_url: str, question: str) -> str:
    """
    调用 GLM-4V 分析图像，返回模型的回答文本
    """
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ],
        temperature=0.1
    )
    return response.choices[0].message.content.strip()

# =======================
# 自动化测试类
# =======================
class TestSutra212Structure(TestCase):

    def test_cover_page_is_wujingtongjuan_not_specific_title(self):
        """
        测试：原目录索引页 038468 是否为“五经同卷”封面，且不包含《菩萨睒子经》等具体经名
        """
        question = f"""
        请分析这张古籍影印图：
        1. 图像中央是否有四个大字？
        2. 这四个字是否是“{SUTRA_INFO['expectedCoverLabel']}”？
        3. 页面上是否出现了“{SUTRA_INFO['title']}”或“菩萨睒子经”等具体经名？
        4. 是否有译者信息（如“西晋”、“失译”等）？
        
        请回答：
        - 如果图像仅为“{SUTRA_INFO['expectedCoverLabel']}”且无其他经名，请以“是的，符合合卷封面特征”开始。
        - 如果出现了具体经名或译者，请以“不是，包含具体信息”开始。
        """

        result = analyze_image_content(SUTRA_INFO["coverImageUrl"], question)
        print(f"【AI 分析结果】{result}")

        # 断言：必须是合卷封面，且不包含具体经名
        self.assertTrue(
            result.startswith("是的，符合合卷封面特征") and 
            "菩萨睒子经" not in result and 
            "西晋" not in result and 
            "失译" not in result,
            f"封面页不应包含具体经名或译者信息，但 AI 检测到异常内容：{result}"
        )

    def test_metadata_page_contains_correct_title(self):
        """
        测试：正文第一页 038469 是否包含正确的经名和译者信息
        """
        question = f"""
        请分析这张古籍影印图：
        1. 是否出现了经名“{SUTRA_INFO['title']}”或“菩萨睒子经”？
        2. 是否出现了译者信息，如“西晋”、“失译”、“附西晋”等？
        
        请回答：
        - 如果出现了经名和译者，请以“是的，包含完整元数据”开始。
        - 否则以“不是，缺少元数据”开始。
        """

        result = analyze_image_content(SUTRA_INFO["metadataImageUrl"], question)
        print(f"【AI 分析结果】{result}")

        self.assertTrue(
            result.startswith("是的，包含完整元数据"),
            f"元数据页应包含经名和译者，但 AI 检测结果为：{result}"
        )

# =======================
# 运行测试
# =======================
if __name__ == '__main__':
    unittest.main(verbosity=2)
