# test_sutra_metadata.py
import unittest
from test_cases import TEST_CASES

# 模拟从数据库或 JSON 文件加载的“实际数据”
# 实际中，这里可能是从 HTML、OCR 结果或数据库中读取
ACTUAL_DATA = {
    5: {"title": "道行般若波罗蜜经", "author": "晋襄阳释道安撰"},
    30: {"title": "佛说法镜经", "author": "后汉安息国优婆塞安玄共沙门严佛调译"},
    85: {"title": "大方广佛华严经普贤菩萨行愿品", "author": "唐罽宾国三藏般若奉诏译"},
    115: {"title": "佛说方等泥洹经", "author": "失译人名附东晋录"},
    128: {"title": "不一定入定入印经", "author": "元魏婆罗门瞿昙般若流支译"},
    137: {"title": "缘生初胜分法本经", "author": "元魏婆罗门瞿昙般若流支译"},
    175: {"title": "大萨遮尼乾子受记经", "author": "元魏婆罗门瞿昙般若流支译"},
    195: {"title": "称赞净土佛摄受经", "author": "唐三藏法师玄奘奉诏译"},
    212: {"cover": "五经同卷", "title": None, "author": None}
}

class TestSutraMetadata(unittest.TestCase):
    """
    佛典元数据校验测试套件
    """

    def test_all_cases(self):
        """批量运行所有测试用例"""
        failures = []
        for case in TEST_CASES:
            try:
                self._run_single_test(case)
            except AssertionError as e:
                failures.append(f"{case['id']}: {str(e)}")
        
        if failures:
            self.fail("\n".join(failures))

    def _run_single_test(self, case):
        """执行单个测试用例"""
        sutra_num = case["sutra_number"]
        actual = ACTUAL_DATA.get(sutra_num)

        with self.subTest(sutra_number=sutra_num):
            if not actual:
                self.fail("未找到该卷数据")

            field = case["field"]
            if field == "title":
                actual_title = actual.get("title")
                expected = case.get("expected_title", case["title"])

                self.assertEqual(actual_title, expected,
                               msg=f"经名错误：应为'{expected}'，实际为'{actual_title}'")

                # 检查禁止前缀
                if case.get("forbidden_prefix"):
                    self.assertFalse(actual_title.startswith(case["forbidden_prefix"]),
                                   msg=f"经名不应以'{case['forbidden_prefix']}'开头")

            elif field == "author":
                actual_author = actual.get("author")
                expected = case["expected_author"]

                self.assertEqual(actual_author, expected,
                               msg=f"译者错误：应为'{expected}'，实际为'{actual_author}'")

                # 检查禁止字符
                if case.get("forbidden_chars"):
                    for char in case["forbidden_chars"]:
                        self.assertNotIn(char, actual_author,
                                       msg=f"译者信息中包含禁用字：{char}")

                # 检查是否以“译”结尾
                if case.get("must_end_with"):
                    self.assertTrue(actual_author.endswith(case["must_end_with"]),
                                  msg=f"译者信息应以'{case['must_end_with']}'结尾")

            elif field == "structure":
                if not case["has_individual_cover"]:
                    cover = actual.get("cover")
                    expected_label = case["cover_label"]
                    self.assertEqual(cover, expected_label,
                                   msg=f"合卷封面应为'{expected_label}'，实际为'{cover}'")
