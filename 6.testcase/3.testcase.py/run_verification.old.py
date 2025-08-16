# run_verification.py
import unittest
import sys
from parser import parse_index  # ✅ 明确导入

if __name__ == '__main__':
    # 可传参强制更新
    force_download = '--force-download' in sys.argv
    if force_download:
        sys.argv.remove('--force-download')

    # 导入测试（确保 parser 被调用）
    from test_sutra_verification import TestSutraVerification

    # 重新设置 force_download
    TestSutraVerification.setUpClass = classmethod(
        lambda cls: setattr(cls, 'suttas', parse_index(force_download=force_download))
    )

    unittest.main()
