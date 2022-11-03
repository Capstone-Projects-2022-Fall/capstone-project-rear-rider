import os
import asyncio
import concurrent.futures
from ipc.child_process import ChildProcess
from ipc.parent_process import ParentProcess


# from leds_child_proc import LedsChildProcess
dir_path = os.path.dirname(os.path.realpath(__file__))



class BluetoothServerChildProcess(ChildProcess):
    # def __init__(self, leds_child_process: LedsChildProcess):
    def __init__(self):
        super().__init__("python {}/bluetooth.py".format(dir_path))
        # self._leds_child_process = leds_child_process
        self._print_header('test')
    
    def _get_name(self) -> str:
        return 'BluetoothServerChildProcess'
    

    def _print_header(self, message: str):
        return super()._print('==== Bluetooth Process ====\n{}'.format(message))

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

    # #############
    # # LED STUFF #
    # #############

    # async def on_led_strobe_on(self):
    #     """
    #     Turn the strobe light effect on.
    #     """
    #     self._print('on_led_strobe_on')
    #     print('fhdai')
    #     await self._leds_child_process.led_strobe_on()


    # async def on_led_strobe_off(self):
    #     """
    #     Turn the strobe light effect off.
    #     """
    #     self._print('on_led_strobe_off')
    #     await self._leds_child_process.led_strobe_off()
    
    # async def is_strobe_on(self):
    #     self._print('is_strobe_on')
    
    # async def is_strobe_on_response(self, strobe_on: bool):
    #     await self.writeline(
    #         'strobe_on\n'
    #         '{}'.format(strobe_on))
    #     # await self._wait_ack('strobe_on')
    
    # async def on_no_on_handler(self):
    #     line = await self.readline()
    #     self._print('on no on handler: {}'.format(line))

    # async def on_help(self):
    #     while True:
    #         line = await self.readline()
    #         if line == '== help_string_end ==':
    #             break
    #     pass

    # def no_on_handler(self, on_command, err):
    #     self._print('no on handler s: {}\n,{}'.format(on_command, err))
    
    # async def on_discoverable(self):
    #     """
    #     The handler for when bluetooth changes its discoverability to other devices.
    #     """
    #     line = await self.readline()
    #     if line == '1':
    #         await self._leds_child_process.set_discoverable_effect(False)
    #     elif line == '0':
    #         await self._leds_child_process.set_discoverable_effect(False)
    
    # async def on_led_config(self):
    #     line = await self.readline()
    #     split = line.split(' ')
    #     self._print(f'led_config: {line}')
    #     await self._leds_child_process.add_led_effect(line)




if __name__ == '__main__':
    # leds_proc = LedsChildProcess()
    # proc = BluetoothServerChildProcess(leds_child_process=leds_proc)
    proc = BluetoothServerChildProcess()
    # parent = TestParent(leds_proc)
    processes: list = [
        proc,
        # leds_proc
    ]
    futures = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # We create a thread for each to-be-executed child process
        # so that asyncio manages one child process per thread.
        for process in processes:
            futures.append(executor.submit(asyncio.run, process.begin()))
    print(len(futures))
    concurrent.futures.wait(futures)
