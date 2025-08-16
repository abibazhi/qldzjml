# run_all_tests.py
import unittest
import sys
from test_text_verification import TestSutraTextVerification
from test_vision_verification import TestSutraVisionVerification

if __name__ == '__main__':
    force_download = '--force-download' in sys.argv
    if force_download:
        sys.argv.remove('--force-download')

    # 设置文本测试的 suttas
    from parser import parse_index
    TestSutraTextVerification.setUpClass = classmethod(
        lambda cls: setattr(cls, 'suttas', parse_index(force_download=force_download))
    )

    # 构建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTest(loader.loadTestsFromTestCase(TestSutraTextVerification))
    suite.addTest(loader.loadTestsFromTestCase(TestSutraVisionVerification))

    # 运行
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # 输出总结
    print("\n" + "="*50)
    print(f"总测试数: {result.testsRun}")
    print(f"失败数: {len(result.failures)}")
    print(f"错误数: {len(result.errors)}")
    if result.wasSuccessful():
        print("🎉 所有校验通过！")
    else:
        print("❌ 存在不一致，请检查报告。")
    print("="*50)
