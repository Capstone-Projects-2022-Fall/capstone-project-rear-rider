## start PYTHONPATH modification
import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__),
                  f'{os.pardir}/..')
)
sys.path.append(PROJECT_ROOT)
## end PYTHONPATH modification
import test_ipc
import unittest

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    suite = unittest.TestSuite()
    suite.addTests(test_ipc.test_cases())
    runner.run(suite)