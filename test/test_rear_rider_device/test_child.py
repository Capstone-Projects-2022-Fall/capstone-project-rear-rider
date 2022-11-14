import asyncio
import sys, os
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__),
                  f'{os.pardir}/..')
)
sys.path.append(PROJECT_ROOT)
from rear_rider_device.ipc.parent_process import ParentProcess


class TestParentProcess(ParentProcess):
    def __init__(self):
        self.log_file = open('./test_log', 'w')

    def pre_ready(self):
        self.log_file.write('pre_ready\n')

    def pre_done(self):
        self.log_file.write('pre_done\n')

if __name__ == "__main__":
    asyncio.run(TestParentProcess().begin())