# test_text_verification.py
import unittest
from parser import parse_index  # ✅ 直接导入
#from test_cases import TEST_CASES


# 在文件顶部添加
import json
import os

# 加载文本测试用例
def load_text_test_cases():
    json_path = os.path.join('test_cases', 'text_cases.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"未找到测试用例文件: {json_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"测试用例 JSON 格式错误: {e}")

# 使用
TEST_CASES = load_text_test_cases()

class TestSutraTextVerification(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # ✅ 在这里调用 parse_index
        cls.suttas = parse_index(force_download=False)  # 或 True 强制更新

    def test_all_verification_rules(self):
        failures = []
        for i, case in enumerate(TEST_CASES):
            try:
                self._apply_rule(case)
            except AssertionError as e:
                failures.append(f"[{i+1:03d}] [{case['id']}] No.{case['sutra_number']}: {str(e)}")
        
        if not failures:
            print(f"\n🎉 所有 {len(TEST_CASES)} 个校验用例全部通过！")
        else:
            self.fail(f"\n❌ 共发现 {len(failures)} 处不一致：\n" + "\n".join(failures))


    def _apply_rule(self, case):
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
