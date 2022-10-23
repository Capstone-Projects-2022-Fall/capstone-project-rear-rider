import asyncio
from ipc.child_process import ChildProcess

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

class BluetoothServerChildProcess(ChildProcess):
    def __init__(self, leds_child_process):
        super().__init__("python {}/bluetooth.py".format(dir_path))

    def _print_header(self, message: str):
        return super()._print('==== Bluetooth Process ====\n{}'.format(message))

    async def on_ready(self):
        self._print('==== Bluetooth Process: on_ready ====')
        await self.writeline('sensor_data_stream')

    def on_done(self):
        self._print('==== Bluetooth : on_done')

    async def on_sensor_data_stream_ready(self):
        self._print_header('sensor_data_stream begin')
        
        self._print_header('sensor_data_stream_end')
    
    async def on_set_data_ack(self):
        self._print('on_set_data_ack')

    async def on_read_accelerometer(self):
        self._print('on_read_accelerometer')

    #############
    # LED STUFF #
    #############

    async def on_led_strobe_on(self):
        self._print('led_strob_on')

    async def on_led_strobe_off(self):
        self._print('led_strobe_off')
    
    async def is_strobe_on(self):
        self._print('is_strobe_on')
    
    async def is_strobe_on_response(self, strobe_on: bool):
        await self.writeline(
            'strobe_on\n'
            '{}'.format(strobe_on))
        await self._wait_ack('strobe_on')
