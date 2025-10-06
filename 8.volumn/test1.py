# test_vision_verification.py
import unittest
import json
from zhipuai import ZhipuAI
from typing import Dict, List

# =======================
# 配置
# =======================
API_KEY = "1404e31679389d3b24f6b9a3fa469157.ZXIFA6ijxoyUpg3Y"  # 替换为您的密钥
MODEL = "glm-4v-flash"

client = ZhipuAI(api_key=API_KEY)

def analyze_image(image_url: str, question: str) -> str:
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
        temperature=0.01
    )
    return response.choices[0].message.content.strip()


imageurl="https://daxumi.cn/qldzj/001/1.png"
question="能不能整理一下这个图片中的目录及其对应页码？"

result = analyze_image(imageurl, question)
print(f"【AI 分析】目录: {result}")

'''
# =======================
# 加载测试用例
# =======================
with open('test_cases/vision_cases.json', 'r', encoding='utf-8') as f:
    VISION_CASES: List[Dict] = json.load(f)

# =======================
# 测试类
# =======================
class TestSutraVisionVerification(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cases = VISION_CASES

    def test_all_vision_rules(self):
        failures = []
        for case in self.cases:
            try:
                self._test_cover_page(case)
                self._test_metadata_page(case)
            except AssertionError as e:
                failures.append(f"[{case['id']}] 编号 {case['sutra_number']}: {str(e)}")
        if failures:
            self.fail("\n".join(failures))

    def _test_cover_page(self, case):
        question = f"""
        请分析这张古籍影印图：
        1. 图像中央是否有四个大字？
        2. 这四个字是否是“{case['expected_cover_label']}”？
        3. 页面上是否出现了“{case['title']}”或“菩萨睒子经”等具体经名？
        4. 是否有译者信息（如“西晋”、“失译”等）？

        请回答：
        - 如果仅为“{case['expected_cover_label']}”且无其他经名，请以“是的，符合合卷封面特征”开始。
        - 否则以“不是，包含具体信息”开始。
        """

        result = analyze_image(case["cover_image_url"], question)
        print(f"【AI 分析】封面 {case['catalog_index_page']}: {result}")

        self.assertTrue(
            result.startswith("是的，符合合卷封面特征"),
            f"封面不应含具体经名，但检测到：{result}"
        )

    def _test_metadata_page(self, case):
        question = f"""
        请分析这张古籍影印图：
        1. 是否出现了经名“{case['title']}”或“菩萨睒子经”？
        2. 是否出现了译者信息，如“西晋”、“失译”、“附西晋”等？

        请回答：
        - 如果出现了经名和译者，请以“是的，包含完整元数据”开始。
        - 否则以“不是，缺少元数据”开始。
        """

        result = analyze_image(case["metadata_image_url"], question)
        print(f"【AI 分析】元数据 {case['metadata_page']}: {result}")

        self.assertTrue(
            result.startswith("是的，包含完整元数据"),
            f"元数据页应含经名和译者，但检测为：{result}"
        )
'''
