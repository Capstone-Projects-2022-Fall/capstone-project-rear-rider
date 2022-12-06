import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
                os.path.dirname(__file__),
                # This file should be in `rear_rider_device/` so we need to travel up one directory.
                f'{os.pardir}')
)
sys.path.append(PROJECT_ROOT)
import test_actuators
import unittest

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    suite = unittest.TestSuite()
    suite.addTests(test_actuators.test_cases())
    runner.run(suite)