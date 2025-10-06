# test_vision_verification.py
import unittest
import json
from zhipuai import ZhipuAI
from typing import Dict, List
from openai import OpenAI

# =======================
# 配置
# =======================
API_KEY = "1404e31679389d3b24f6b9a3fa469157.ZXIFA6ijxoyUpg3Y"  # 替换为您的密钥
MODEL = "glm-4v-flash"


client = ZhipuAI(api_key=API_KEY)

def analyze_image(image_url: str, question: str) -> str:
    image_response = client.chat.completions.create(
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
    # 获取图片识别结果
    image_result = image_response.choices[0].message.content.strip()

    print(f"图片识别结果：\n\n{image_result}")
    print("前面50个字符：")
    print(image_result[0:50])
    begin_of_image_result = image_result[0:50]

    # 第二次调用：根据识别结果进行进一步判断
    judge_prompt = "请用json格式输出经名和卷号。没有就输出空"

    clientDeepseek = OpenAI(
        #api_key=os.environ.get('DEEPSEEK_API_KEY'),
        api_key='sk-570772014b0447efbfc9b1f577d7d86b',
        base_url="https://api.deepseek.com")

    judge_response = clientDeepseek.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content":  f"{judge_prompt}\n\n：{begin_of_image_result}"},
        ],
        stream=False
    )
    return judge_response.choices[0].message.content.strip()
    
    #judge_response = client.chat.completions.create(
    #    model=MODEL,
    #    messages=[
    #        {
    #            "role": "user",
    #            "content": f"{judge_prompt}\n\n：{image_result}"
    #        }
    #    ],
    #    temperature=0.01
    #)



imageurl="https://daxumi.cn/qldzj/001/326.png"
question="请问这个图片是不是一卷的开始页？开始页最右侧第一列应该是经名+卷号，比如大般若波罗蜜多经卷第一百五十二。"

imageurl="https://daxumi.cn/qldzj/001/327.png"
question="请问这个图片是不是一卷的开始页？开始页最右侧第一列应该是经名+卷号，比如大般若波罗蜜多经卷第一百五十二。请回答是或否，然后给出最右侧第一列的文字"

imageurl="https://daxumi.cn/qldzj/001/328.png"
question="乾隆大藏经中的一卷经文的开始页，最右侧第一列应该是经名+卷号，比如大般若波罗蜜多经卷第一百五十二。请先识别最右侧第一列的文字内容，然后再根据文字内容推理该图片是否是一个卷的第一页"
'''
(zhipu) jm@X2024:~/github/qldzjml/8.volumn$ python isBeginPage.py
【AI 分析】目录: 最右侧第一列的文字内容是“新雕乾隆大藏經”，没有显示卷号和经名。

由于没有具体的经名和卷号信息，无法确定这是否是一个卷的第一页。通常情况下，卷的第一页会明确标注经名和卷号，但在这张图片中并没有这样的信息。因此，仅凭现有的信息无法判断这页是否为某部经典的第一页。
'''

imageurl="https://daxumi.cn/qldzj/001/328.png"
question="乾隆大藏经中的一卷经文的开始页，最右侧第一列应该是经名+卷号，比如大般若波罗蜜多经卷第一百五十二。请先识别最右>侧第一列的文字内容，然后再根据文字内容推理该图片是否是一个卷的第一页"  


imageurl="https://daxumi.cn/qldzj/001/326.png"
question="乾隆大藏经中的一卷经文的开始页，最右侧第一列应该是经名+卷号，比如大般若波罗蜜多经卷第一百五十二。请先识别最右>侧第一列的文字内容，然后再根据文字内容推理该图片是否是一个卷的第一页"  

imageurl="https://daxumi.cn/qldzj/001/326.png"
question="请先识别图片最右侧的开始几列的文字内容。如果包括经名+卷号，比如大般若波罗蜜多经卷第一百五十二，就说明是一卷经文的第一列。请判断"  


imageurl="https://daxumi.cn/qldzj/001/326.png"
question="请先识别图片最右侧的开始5列的文字内容。如果包括经名+卷号，比如大般若波罗蜜多经卷第一百五十二，就说明是一卷经文的第一列。请判断并输出是或否"  


imageurl="https://daxumi.cn/qldzj/001/327.png"
question="请先识别图片最右侧的开始5列的文字内容。如果包括经名+卷号，比如大般若波罗蜜多经卷第一百五十二，就说明是一卷经文的第一列。请输出前5列内容后，再判断并输出是或否"  

imageurl="https://daxumi.cn/qldzj/001/327.png"
question="请先识别图片最右侧的开始5列的文字内容。如果包括经名+卷号，比如大般若波罗蜜多经卷第一百五十二，就说明是一卷经文的第一页。请输出前5列内容后，再根据内容推理并输出是否是第一页？"  


imageurl="https://daxumi.cn/qldzj/001/328.png"
question="请先识别图片最右侧的开始5列的文字内容。如果包括经名+卷号，比如大般若波罗蜜多经卷第一百五十二，就说明是一卷经文的第一页。请输出前5列内容后，再根据内容推理并输出是否是第一页？"  


imageurl="https://daxumi.cn/qldzj/001/394.png"
question="请先识别图片最右侧的开始5列的文字内容。如果包括经名+卷号，比如大般若波罗蜜多经卷第一百五十二。请输出前5列内容后，再根据内容推理并输出是否包括经名和卷号？"  

imageurl="https://daxumi.cn/qldzj/001/395.png"
question="请先识别图片最右侧的开始5列的文字内容。如果包括经名+卷号，比如大般若波罗蜜多经卷第一百五十二。请输出前5列内容后，再根据内容推理并输出是否包括经名和卷号？"  


imageurl="https://daxumi.cn/qldzj/001/394.png"
question="请先识别图片最右侧的开始几列的文字内容,并打印出来。如果包括经名+卷号，比如大般若波罗蜜多经卷第一百五十二。请推理后用json格式输出经名和卷号"  


imageurl="https://daxumi.cn/qldzj/001/394.png"
question="请先识别图片最右侧的开始几列的文字内容,并打印出来。如果包括经名+卷号，比如大般若波罗蜜多经卷第一百五十二。请推理后用json格式输出经名和卷号"  


imageurl="https://daxumi.cn/qldzj/001/394.png"
question="请识别图片中方框内最右侧一列的文字,并打印出来。如果包括经名+卷号，比如大般若波罗蜜多经卷第一百五十二。请推理后用json格式输出经名和卷号"  


imageurl="https://daxumi.cn/qldzj/001/394.png"
question="请识别图片中所有文字并打印出来"  


imageurl="https://daxumi.cn/qldzj/001/394.png"
question="请识别图片中所有文字并打印出来"  

result = analyze_image(imageurl, question)
print(f"{result}")








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
