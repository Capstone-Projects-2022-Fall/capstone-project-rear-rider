import asyncio
from datetime import datetime
from turtle import distance
from ipc.child_process import ChildProcess
from typing import Deque
from bluetooth_server_child_proc import BluetoothServerChildProcess
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))

class LidarChildProcess(ChildProcess):
    def __init__(self, bt_server_proc: BluetoothServerChildProcess, buf_size: int = 64, fps: int = 60):
        """
        Default `buf_size` of 64 frame datapoints at 60 `fps`.
        """
        super().__init__('python {}/lidar_proc.py'.format(dir_path))
        self.cyclic_buff = Deque[tuple[float, float, float]](maxlen=buf_size)
        self.fps = fps
        self.ready = asyncio.Future()
        self.bt_server_proc = bt_server_proc
    
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
        self._print('on_data {}/{} fps: {} start: {} current: {}'.format(
            len(self.cyclic_buff), 
            self.cyclic_buff.maxlen,
            self.fps,
            self.start_time.strftime('%x %X.%f'),
            datetime.now().strftime('%x %X.%f'),
        ))
        lidar_data = await self.readline()
        self._print(
            '{}\n'
            '\t{}\n'.format(
                lidar_data[0],
                lidar_data[1],
            )
        )

        
        data = (
            float((lidar_data[0]* 0.01)),
            float(lidar_data[1]),
        )
        self.cyclic_buff.append(data)
        await self.bt_server_proc.writeline(
            'set_data\n'
            'lidar\n'
            '{},{}'.format(data[0], data[1]))
        await asyncio.sleep(1.0/self.fps)
        await self.writeline('get_data')
