import sys
import os
import threading
PROJECT_ROOT = os.path.abspath(os.path.join(
                os.path.dirname(__file__),
                # This file should be in `rear_rider_device/` so we need to travel up one directory.
                f'{os.pardir}')
)
sys.path.append(PROJECT_ROOT)

import asyncio
import concurrent.futures
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Any, Callable, Union

from rear_rider_device.ipc.parent_process import ParentProcess
from rear_rider_device.rear_rider_bluetooth_server.src.services.characteristics.strobe_light import StrobeLight
import rear_rider_device.rear_rider_bluetooth_server.src.main as bt_server_main
from rear_rider_device.rear_rider_bluetooth_server.src.services.hello_world import RearRiderConfig

DATA_FUTURE_TIMEOUT = 0.016
'''
The amount of seconds to wait for future data.
'''

class BluetoothParentProcess(ParentProcess):
    rear_rider_bt: bt_server_main.RearRiderBluetooth
    strobe_light: StrobeLight
    _help_message = (
            'help\n'
            '== Help ==\n'
            'set_data\nhelp\n== help_string_end ==')
    def __init__(self, bluetooth_ready: Future, create_strobe_light: Callable[[Any],StrobeLight]):
        self._bluetooth_ready = bluetooth_ready
        self.strobe_light = create_strobe_light(self)
        self._accel_data_cond = threading.Condition()
        self._accel_data: Union[None, tuple[float, float, float]] = None


    async def pre_ready(self):
        print('pre_ready')
        self._bluetooth_ready.result(2.5)
        ####################################################
        # FOR DEBUGGING ONLY
        # self._bluetooth_ready.result() # FOR DEBUGGING ONLY
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        ####################################################
        def on_rear_rider_config(cfg: RearRiderConfig):
            self.writeline(f'led_config\n{cfg.pattern} {cfg.brightness} {cfg.color[0]} {cfg.color[1]} {cfg.color[2]}')
            self.writeline(f'lidar_config\b{cfg.lidar_unsafe_distance}')
        self.rear_rider_bt.hello_world_svc.config_chr.set_on_config(on_rear_rider_config)
        self.rear_rider_bt.sensors_svc.accelerometer_characteristic.set_read_accelerometer_cb(self.read_accelerometer)
        self.writeline('bluetooth_is_ready')
    
    async def pre_loop(self):
        self.rear_rider_bt.set_on_discoverable_changed(self.discoverable_changed)

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
            # TODO: Add critical section guard here
            # self.writeline('set_data_ack')
            with self._accel_data_cond:
                self._accel_data = _parse_acceleration_data(await self.readline())
                self._accel_data_cond.notify_all()
        elif data_type_line == 'lidar':
            data = await self.readline()
            self.rear_rider_bt.hello_world_svc.lidar_chr.value = data
            self.rear_rider_bt.hello_world_svc.lidar_chr.check_object_in_range()
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
        # TODO: Add critical section guard in this block
        self.writeline('is_strobe_on')
        return bool(self.readline_sync())
    
    def discoverable_changed(self, value: str):
        timeout = self.rear_rider_bt.get_discoverable_timeout()
        self.writeline(f'discoverable\n{value} {timeout}')

    def read_accelerometer(self) -> tuple[float, float, float]:
        '''
        This action could timeout.
        '''
        with self._accel_data_cond:
            self.writeline('read_accelerometer')
            try:
                self._accel_data_cond.wait(DATA_FUTURE_TIMEOUT)
                if self._accel_data is None:
                    raise Exception('Acceleration data was None')
                return self._accel_data
            finally:
                self._accel_data = None
        
def _parse_acceleration_data(line: str):
    nums = line.split(',')
    return (float(nums[0]),float(nums[1]),float(nums[2]))

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
                def bluetooth_is_ready(rear_rider_bt: bt_server_main.RearRiderBluetooth):
                    proc.rear_rider_bt = rear_rider_bt
                    proc._bluetooth_ready.set_result(None)

                bt_server_main.main(print,
                        on_ready=bluetooth_is_ready,
                        strobe_light=proc.strobe_light,
                )

            futures.append(executor.submit(asyncio.run, bt_server_main_task_co()))
        concurrent.futures.wait(futures)
    # Begin session with the parent process. The parent process is collecting the data.
    asyncio.run(main())
