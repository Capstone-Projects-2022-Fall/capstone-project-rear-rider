import asyncio
import threading
from datetime import datetime
from rear_rider_device.ipc.child_process import ChildProcess
from typing import Deque

from rear_rider_device.bluetooth_server_child_proc import BluetoothServerChildProcess

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

class AccelerometerChildProcess(ChildProcess):
    def __init__(self, bt_server_proc: BluetoothServerChildProcess, buf_size: int = 64, fps: int = 60):
        """
        Default `buf_size` of 64 frame datapoints at 60 `fps`.
        """
        super().__init__('python {}/accel_proc.py'.format(dir_path))
        self.cyclic_buff = Deque[tuple[float, float, float]](maxlen=buf_size)
        self.fps = fps
        self.ready = asyncio.Future()
        self.bt_server_proc = bt_server_proc
        self._data_cond = threading.Condition()
    
    async def on_ready(self):
        self.start_time = datetime.now()
        self._print('AccelerometerChildProcess is ready.')
        async def read_accelerometer():
            await self.writeline('get_data')
            with self._data_cond:
                self._data_cond.wait(0.016)
                return self.cyclic_buff.pop()
        self.bt_server_proc.set_read_accelerometer_cb(read_accelerometer)
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
        vector = await self.readline()
        tapped = await self.readline()
        motion = await self.readline()
        await self.readline()
        # self._print(
        #     '{}\n'
        #     '\t{}\n'
        #     '\t{}'.format(
        #         vector,
        #         tapped,
        #         motion
        #     )
        # )

        component = vector.split(' ')
        data = (
            float(component[0]),
            float(component[1]),
            float(component[2])
        )
        with self._data_cond:
            self.cyclic_buff.append(data)
            self._data_cond.notify_all()
    
    def _get_name(self) -> str:
        return 'AccelerometerChildProcess'
    
    async def on_exception(self):
        line = await self.readline()
        self._print(f'Exception: {line}')
