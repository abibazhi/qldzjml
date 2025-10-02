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



# ... 其他代码保持不变 ...

    def _apply_rule(self, case):
        num = case['sutra_number']
        sutra = self.suttas.get(num)
        self.assertIsNotNone(sutra, f"编号 {num} 的佛典未找到")

        case_type = case.get('type', 'metadata-consistency')  # 获取类型

        with self.subTest(id=case['id'], number=num):
            if case_type == "link-target":
                self._test_link_target(sutra, case)
            elif case_type == "special-structure":
                self._test_special_structure(sutra, case)
            elif case.get('field') == 'title':
                self._test_title_rule(sutra, case)
            elif case.get('field') == 'author':
                self._test_author_rule(sutra, case)
            # ... 其他类型可继续扩展

    def _test_link_target(self, sutra, case):
        """专门处理链接目标校验"""
        expected = case['expected_start_page']
        actual = sutra.start_page  # ✅ 从 parse_index() 解析出的真实值

        self.assertEqual(
            actual, expected,
            msg=f"🔗 链接起始页错误：\n"
                f"  经{case['sutra_number']}《{case['title']}》\n"
                f"  期望: {expected} ← 应指向封面\n"
                f"  实际: {actual} ← 当前指向\n"
                f"  💡 {case.get('note', '')}"
        )

    def _test_title_rule(self, sutra, case):
        """原 title 校验逻辑抽离"""
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

    def _test_author_rule(self, sutra, case):
        """原 author 校验逻辑抽离"""
        expected = case['expected_author']
        self.assertEqual(sutra.author, expected,
                       msg=f"译者错误：应为'{expected}'，实际为'{sutra.author}'")

        case_type = case.get('type')

        if case_type == "authoritative-correction":
            # 如果系统中无作者，允许（因底本无署名）
            if not sutra.author or sutra.author.strip() == "":
                # 可选：打印提示
                print(f"📌 T142: 原无译者署名，当前为空，合理。")
                return  # ✅ 不报错

            # 如果有作者，则必须等于权威认定值
            #expected = case['expected_author']
            self.assertEqual(
                sutra.author, expected,
                msg=f"若显示译者，必须为权威认定形式：\n"
                    f"  应为: '{expected}'\n"
                    f"  实际: '{sutra.author}'\n"
                    f"  💡 {case['note']}"
            )

        # ✅ 新增：必须包含某子串
        if case.get('must_contain'):
            sub_str = case['must_contain']
            self.assertIn(
                sub_str, sutra.author,
                msg=f"译者信息应包含'{sub_str}'，实际为'{sutra.author}'"
            )

        # ✅ 新增：不能是某个错误形式
        if case.get('must_not_be'):
            forbidden_form = case['must_not_be']
            self.assertNotEqual(
                sutra.author, forbidden_form,
                msg=f"译者信息不应为'{forbidden_form}'，这是常见错误形式"
            )



        if case.get('forbidden_chars'):
            for char in case['forbidden_chars']:
                self.assertNotIn(char, sutra.author,
                               msg=f"译者信息中包含禁用字：{char}")

        if case.get('must_end_with'):
            self.assertTrue(sutra.author.endswith(case['must_end_with']),
                          msg=f"译者信息应以'{case['must_end_with']}'结尾")

 # ... 其他方法 ...

    def _test_special_structure(self, sutra, case):
        """验证特殊装帧结构"""
        cover_label = case.get('cover_label')
        has_individual_cover = case.get('has_individual_cover', True)

        # 示例：可以检查封面标签是否符合预期
        if cover_label:
            # 假设您有办法获取封面信息（如从图像元数据或目录）
            # 这里先用一个占位断言
            pass  # TODO: 实际封面标签校验逻辑（可后续扩展）

        # 示例：可以记录这是一个特殊结构，避免误报
        if not has_individual_cover:
            # 可用于跳过某些校验，或记录日志
            self._log_or_skip_if_needed(sutra, case)

    def _log_or_skip_if_needed(self, sutra, case):
        """可在此处理：遇到无独立封面的经，跳过某些校验"""
        print(f"📌 注意: 经{case['sutra_number']}《{sutra.title}》为合卷结构，五卷及以上通常无经名及译者信息")
        # 可在此添加逻辑：如跳过“封面译者缺失”等误报

'''
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
'''
