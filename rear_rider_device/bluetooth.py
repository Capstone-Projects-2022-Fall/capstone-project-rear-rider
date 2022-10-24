import asyncio
import concurrent.futures
from concurrent.futures import Future, ThreadPoolExecutor
from pkgutil import get_data
import readline
from sys import stdout, path
from typing import Any, Callable, Union


path.append("rear_rider_bluetooth_server/src/")
path.append("rear_rider_bluetooth_server/src/services")
path.append("rear_rider_bluetooth_server/src/services/characteristics")

from rear_rider_bluetooth_server.src.services.characteristics.strobe_light import StrobeLight
from rear_rider_bluetooth_server.src.services.sensors import SensorsService
from ipc.parent_process import ParentProcess
import rear_rider_bluetooth_server.src.main as bt_server_main
from rear_rider_bluetooth_server.src.services.hello_world import HelloWorldService

class BluetoothParentProcess(ParentProcess):
    hello_world_service: Union[None, HelloWorldService]
    sensors_service: Union[None, SensorsService]
    strobe_light: StrobeLight
    _help_message = (
            'help\n'
            '== Help ==\n'
            'set_data\nhelp\n== help_string_end ==')
    def __init__(self, bluetooth_ready: Future, create_strobe_light: Callable[[Any],StrobeLight]):
        self._bluetooth_ready = bluetooth_ready
        self.strobe_light = create_strobe_light(self)

    async def pre_ready(self):
        print('pre_ready')
        self._bluetooth_ready.result(2.5)
        ####################################################
        # FOR DEBUGGING ONLY
        # self._bluetooth_ready.result() # FOR DEBUGGING ONLY
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        ####################################################
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
            # TODO: Add critical section guard here
            # self.writeline('set_data_ack')
            nums = data.split(',')
            self.sensors_service.accelerometer_characteristic.vector = (
                float(nums[0]),float(nums[1]),float(nums[2]))
        else:
            # TODO: Add critical section guard here
            # self.writeline('set_data_ack')
            pass
    
    async def on_help(self):
        # TODO: Add critical section guard here
        self.writeline(self._help_message)
    
    def turn_on_strobe_light(self):
        # TODO: Add critical section guard here
        self.writeline('led_strobe_on')
    
    def turn_off_strobe_light(self):
        # TODO: Add critical section guard here
        self.writeline('led_strobe_off')
    
    def is_strobe_on(self):
        try:
            # TODO: Add critical section guard in this block
            self.writeline('is_strobe_on')
            return bool(self.readline_sync())
        finally:
            # self.writeline('strobe_on_ack')
            pass


if __name__ == '__main__':
    # TODO: Synchronize writes to stdout using `with` keyword:
    #    https://stackoverflow.com/a/45669280
    async def main():
        bluetooth_ready = Future()

        def create_strobe_light(bt_parent_proc: BluetoothParentProcess):
            """
            Create a strobe light object and set its owner as bt_parent_proc
            """
            return StrobeLight(
                turn_on=bt_parent_proc.turn_on_strobe_light,
                turn_off=bt_parent_proc.turn_off_strobe_light,
                is_on=bt_parent_proc.is_strobe_on,
                frequency=5
            )

        proc = BluetoothParentProcess(bluetooth_ready, create_strobe_light)

        futures = [] # TODO: These futures are never awaited. await them at an appropriate point.
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
                bt_server_main.main(print,
                        on_ready=bluetooth_is_ready,
                        on_read=on_read,
                        strobe_light=proc.strobe_light
                )

            futures.append(executor.submit(asyncio.run, bt_server_main_task_co()))
        concurrent.futures.wait(futures)
    # Begin session with the parent process. The parent process is collecting the data.
    asyncio.run(main())
