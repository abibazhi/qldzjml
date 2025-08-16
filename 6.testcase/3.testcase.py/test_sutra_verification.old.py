# test_sutra_verification.py
import unittest
from parser import parse_index
from test_cases import TEST_CASES
from sutra import Sutra

class TestSutraVerification(unittest.TestCase):
    suttas: dict[int, Sutra] = {}

    @classmethod
    def setUpClass(cls):
        """只运行一次：加载所有佛典数据"""
        sutra_list = parse_index(force_download=False)  # 可设为 True 强制更新
        cls.suttas = {s.number: s for s in sutra_list}

    def test_all_verification_rules(self):
        """运行所有校验规则"""
        failures = []
        for case in TEST_CASES:
            try:
                self._apply_rule(case)
            except AssertionError as e:
                failures.append(f"[{case['id']}] 编号 {case['sutra_number']}: {str(e)}")
        
        if failures:
            self.fail("\n".join(failures))

    def _apply_rule(self, case):
        """应用单条校验规则"""
        num = case['sutra_number']
        sutra = self.suttas.get(num)
        self.assertIsNotNone(sutra, f"编号 {num} 的佛典未找到")

        with self.subTest(id=case['id'], number=num):
            field = case.get('field', 'author')

            if field == 'title':
                expected = case.get('expected_title', case['title'])
                self.assertEqual(sutra.title, expected,
                               msg=f"经名错误：应为'{expected}'，实际为'{sutra.title}'")

                if case.get('forbidden_prefix'):
                    self.assertFalse(sutra.title.startswith(case['forbidden_prefix']),
                                   msg=f"不应以'{case['forbidden_prefix']}'开头")

                if case.get('required_char') and case['required_char'] not in sutra.title:
                    self.fail(f"经名缺少必要字符：{case['required_char']}")

                if case.get('forbidden_char') and case['forbidden_char'] in sutra.title:
                    self.fail(f"经名包含禁用字符：{case['forbidden_char']}")

            elif field == 'author':
                expected = case['expected_author']
                self.assertEqual(sutra.author, expected,
                               msg=f"译者错误：应为'{expected}'，实际为'{sutra.author}'")

                if case.get('forbidden_chars'):
                    for char in case['forbidden_chars']:
                        self.assertNotIn(char, sutra.author,
                                       msg=f"译者信息中包含禁用字：{char}")

                if case.get('must_end_with'):
                    self.assertTrue(sutra.author.endswith(case['must_end_with']),
                                  msg=f"译者信息应以'{case['must_end_with']}'结尾")

            elif field == 'page':
                # 示例：可添加页码相关规则
                self.assertNotEqual(sutra.start_page, "", "起始页码为空")
                self.assertNotEqual(sutra.end_page, "", "结束页码为空")
                if case.get('min_pages'):
                    min_pages = int(case['min_pages'])
                    pages = int(sutra.end_page) - int(sutra.start_page) + 1
                    self.assertGreaterEqual(pages, min_pages,
                                          msg=f"页数少于最低要求 {min_pages}，实际 {pages}")

            elif field == 'structure':
                if not case.get('has_individual_cover', True):
                    # 可结合 section 字段判断是否属于合卷
                    pass  # 您可根据逻辑扩展
