import os
import sys
sys.path.append("../rear_rider_device")

import test_actuators
import unittest

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    suite = unittest.TestSuite()
    suite.addTests(test_actuators.test_cases())
    runner.run(suite)