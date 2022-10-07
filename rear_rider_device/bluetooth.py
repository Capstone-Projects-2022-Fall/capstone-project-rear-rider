import asyncio
from concurrent.futures import Future, ThreadPoolExecutor
from pkgutil import get_data
import readline
from sys import stdout, path
from typing import Union

path.append("rear_rider_bluetooth_server/src/")

from rear_rider_bluetooth_server.src.services.sensors import SensorsService
from ipc.parent_process import ParentProcess
import rear_rider_bluetooth_server.src.main as bt_server_main
from rear_rider_bluetooth_server.src.services.hello_world import HelloWorldService

class BluetoothParentProcess(ParentProcess):
    hello_world_service: Union[None, HelloWorldService]
    sensors_service: Union[None, SensorsService]
    _help_message = (
            'help\n'
            '== Help ==\n'
            'set_data\nhelp')
    def __init__(self, bluetooth_ready: Future):
        self._bluetooth_ready = bluetooth_ready

    async def pre_ready(self):
        print('pre_ready')
        self._bluetooth_ready.result(2.5)
        pass

    def pre_done(self):
        pass
    
    def no_ack(self):
        pass
    
    def no_on_handler(self, on_command, err):
        self.writeline('no_on_handler\n{}'.format(
            self._help_message
        ))
        pass

    async def on_set_data(self):
        data_type_line = await self.readline()

        if data_type_line == 'accelerometer':
            data = await self.readline()
            self.writeline('set_data_ack')
            nums = data.split(',')
            self.sensors_service.accelerometer_characteristic.vector = (
                float(nums[0]),float(nums[1]),float(nums[2]))
        else:
            self.writeline('set_data_ack')
            pass
    
    async def on_help(self):
        self.writeline(self._help_message)

if __name__ == '__main__':
    async def main():
        bluetooth_ready = Future()
        proc = BluetoothParentProcess(bluetooth_ready=bluetooth_ready)

        futures = []
        with ThreadPoolExecutor() as executor:
            futures.append(executor.submit(asyncio.run, proc.begin()))

            async def bt_server_main_task_co():
                def bluetooth_is_ready(hello_world_service: HelloWorldService, sensors_service: SensorsService):
                    proc.hello_world_service = hello_world_service
                    proc.sensors_service = sensors_service
                    print('bluetooth_is_ready')
                    proc._bluetooth_ready.set_result(None)

                x=0
                y=0
                def on_read():
                    x = x + 1
                    y = y + 1
                    return '{},{}'.format(x, y)
                
                bt_server_main.main(print, on_ready=bluetooth_is_ready,
                        on_read=on_read)

            futures.append(executor.submit(asyncio.run, bt_server_main_task_co()))
        pass
    # Begin session with the parent process. The parent process is collecting the data.
    asyncio.run(main())
