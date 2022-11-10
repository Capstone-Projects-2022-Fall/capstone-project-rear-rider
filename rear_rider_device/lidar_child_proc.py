import asyncio
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from datetime import datetime
from rear_rider_device.ipc.child_process import ChildProcess
from rear_rider_device.leds_child_proc import LedsChildProcess
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))

class LidarChildProcess(ChildProcess):

    lidar_distance = 0 # default unit is cm
    signal_strength = 0 # signal unreliable under 100 

    def __init__(self, led_child_proc: LedsChildProcess):
        """
        Default `buf_size` of 64 frame datapoints at 60 `fps`.
        """
        super().__init__('sudo python {}/lidar_proc.py'.format(dir_path))
        self.ready = asyncio.Future()
        self.led_child_proc = led_child_proc
        
    
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
        lidar_distance = lidar_data[0]
        signal_strength = lidar_data[1]
        self._print('Lidar_distance:{}\n\tSignal_strength:{}\n'.format(lidar_distance, signal_strength))
        
        unsafe_distance = 50 
        if int(lidar_distance) < unsafe_distance:
            await self.led_child_proc.led_strobe_on()
        else:
            await self.led_child_proc.led_strobe_off()
        
        await asyncio.sleep(1.0/100)
        await self.writeline('get_data')
    
    def no_on_handler(self, on_command, err):
        self._print(f'no_on_handler(): {on_command}\n{err}')
    
    def _get_name(self) -> str:
        return 'LidarChildProcess'

class test_lidar_proc(LidarChildProcess):
    def __init__(self):
        super().__init__()
        self._program = 'python {}/test_lidar_proc.py'.format(dir_path)
    
    def _get_name(self) -> str:
        return 'test_lidar_proc'

if(__name__ == "__main__"):
    async def main():
        leds = LedsChildProcess()
        lidar_child_process = LidarChildProcess(led_child_proc=leds)
        futures = [] # TODO: These futures are never awaited. await them at an appropriate point.
        with ThreadPoolExecutor() as executor:
            futures.append(executor.submit(asyncio.run, lidar_child_process.begin()))
            futures.append(executor.submit(asyncio.run, leds.begin()))
        concurrent.futures.wait(futures)
    # Begin session with the parent process. The parent process is collecting the data.
    asyncio.run(main())
