import os
from typing import Awaitable, Callable, Union
from rear_rider_device.ipc.child_process import ChildProcess
from rear_rider_device.leds_child_proc import LedsChildProcess
dir_path = os.path.dirname(os.path.realpath(__file__))

class BluetoothServerChildProcess(ChildProcess):
    '''
    This class handles the messages received from the bluetooth server child process.
    '''
    def __init__(self, leds_child_process: LedsChildProcess):
        super().__init__(f'python {dir_path}/bluetooth.py')
        self._leds_child_process = leds_child_process
        self._read_accelerometer_cb: Union[None, Callable[[], Awaitable[tuple[float, float, float]]]] = None

    def _get_name(self) -> str:
        return 'BluetoothServerChildProcess'

    def _print_header(self, message: str):
        return super()._print(f'==== Bluetooth Process ====\n{message}')

    async def on_wait_ready(self):
        while True:
            line = await self.readline()
            if line == 'bluetooth_is_ready':
                break

    async def on_ready(self):
        self._print('==== Bluetooth Process: on_ready ====')

    def on_done(self):
        self._print('==== Bluetooth : on_done')

    async def on_sensor_data_stream_ready(self):
        self._print_header('sensor_data_stream begin')
        self._print_header('sensor_data_stream_end')

    async def on_set_data_ack(self):
        self._print('on_set_data_ack')

    async def on_read_accelerometer(self):
        self._print('on_read_accelerometer')
        accel = await self._read_accelerometer()
        await self.writeline(
            'set_data\n'
            'accelerometer\n'
            f'{accel[0]},{accel[1]},{accel[2]}')

    async def _read_accelerometer(self):
        read_accelerometer_cb = self._read_accelerometer_cb
        if read_accelerometer_cb is None:
            raise Exception('The read_accelerometer_cb is None')
        return await read_accelerometer_cb()

    def set_read_accelerometer_cb(self, callback: Callable[[], Awaitable[tuple[float, float, float]]]):
        self._read_accelerometer_cb = callback

    #############
    # LED STUFF #
    #############

    async def on_led_strobe_on(self):
        """
        Turn the strobe light effect on.
        """
        self._print('on_led_strobe_on')
        print('fhdai')
        await self._leds_child_process.led_strobe_on()


    async def on_led_strobe_off(self):
        """
        Turn the strobe light effect off.
        """
        self._print('on_led_strobe_off')
        await self._leds_child_process.led_strobe_off()

    async def is_strobe_on(self):
        self._print('is_strobe_on')

    async def is_strobe_on_response(self, strobe_on: bool):
        await self.writeline(
            'strobe_on\n'
            f'{strobe_on}')

    async def on_no_on_handler(self):
        line = await self.readline()
        self._print(f'on no on handler: {line}')

    async def on_help(self):
        while True:
            line = await self.readline()
            if line == '== help_string_end ==':
                break

    def no_on_handler(self, on_command, err):
        self._print(f'no on handler s: {on_command}\n,{err}')

    async def on_discoverable(self):
        """
        The handler for when bluetooth changes its discoverability to other devices.
        """
        vals = (await self.readline()).split(' ')
        discoverable = vals[0]
        self._print(f'Discoverable: {discoverable} ; Timeout: {vals[1]}')
        if discoverable == '1':
            await self._leds_child_process.set_discoverable_effect(True)
        elif discoverable == '0':
            await self._leds_child_process.set_discoverable_effect(False)

    async def on_led_config(self):
        line = await self.readline()
        self._print(f'led_config: {line}')
        await self._leds_child_process.add_led_effect(line)
