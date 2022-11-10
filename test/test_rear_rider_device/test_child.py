import asyncio
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