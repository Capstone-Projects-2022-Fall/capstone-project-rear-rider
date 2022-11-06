from ast import main
import asyncio
from datetime import datetime
from turtle import distance
from ipc.child_process import ChildProcess
from typing import Deque
from bluetooth_server_child_proc import BluetoothServerChildProcess
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))

class LidarChildProcess(ChildProcess):
    def __init__(self):
        """
        Default `buf_size` of 64 frame datapoints at 60 `fps`.
        """
        super().__init__('python {}/lidar_proc.py'.format(dir_path))
        self.ready = asyncio.Future()
    
    async def on_ready(self):
        self.start_time = datetime.now()
        self._print('LidarChildProcess is ready.')
        # try:
            # await self.writeline('ready_ack')
        try:
            await self.writeline('get_data')
        except:
            pass
        self.ready.set_result(None)
        self._print('after_on_ready')

    async def on_data(self):
        lidar_data = (await self.readline()).split(' ')
        self._print(
            '{}\n'
            '\t{}\n'.format(
                lidar_data[0],
                lidar_data[1]
            )
        )
        
        # Needs to send led notification
        # await self.bt_server_proc.writeline(
            # if lidar_data < some distance:
            #     self.led_child_proc
        #     'set_data\n'
        #     'lidar\n'
        #     '{},{}'.format(data[0], data[1]))
        await asyncio.sleep(1.0/100)
        await self.writeline('get_data')

class test_lidar_proc(LidarChildProcess):
    def __init__(self):
        super().__init__()
        self._program = 'python {}/test_lidar_proc.py'.format(dir_path)

if(__name__ == "__main__"):
    myTest=test_lidar_proc()
    asyncio.run(myTest.begin())
