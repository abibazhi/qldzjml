# run_verification.py
import unittest
import sys
from test_sutra_verification import TestSutraVerification

if __name__ == '__main__':
    # 修改 setUpClass 行为
    if '--force-download' in sys.argv:
        sys.argv.remove('--force-download')
        TestSutraVerification.setUpClass = classmethod(
            lambda cls: setattr(cls, 'suttas', parse_index(force_download=True))
        )

    unittest.main()
