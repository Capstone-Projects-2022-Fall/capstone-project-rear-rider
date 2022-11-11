import asyncio
import concurrent.futures
from typing import Union
from rear_rider_device.ipc.child_process import ChildProcess

import os
import threading

from rear_rider_device.ipc.parent_process import ParentProcess 
dir_path = os.path.dirname(os.path.realpath(__file__))

DEFAULT_STROBE_VALUE = '5 0'
"""
5 times per second for 0 seconds

0 seconds == indefinite amount of time.
"""

class LedsChildProcess(ChildProcess):
    def __init__(self):
        super().__init__("sudo python {}/leds_proc.py".format(dir_path))
        self._ready = False
        self._ready_cond = threading.Condition()
        self._strobe_on_lock = threading.Lock()
        self._strobe_on_future: Union[None, concurrent.futures.Future[bool]] = None


    def _get_name(self) -> str:
        return 'LedsChildProcess'

    def _print_header(self, message: str):
        return super()._print('==== Leds Process ====\n{}'.format(message))

    async def on_ready(self):
        with self._ready_cond:
            self._print('==== Leds Process: on_ready ====')
            self._ready = True
            self._ready_cond.notify_all()
    
    def wait_ready(self):
        """
        Wait until the leds child process is ready.
        """
        with self._ready_cond:
            while not self._ready:
                self._ready_cond.wait()

    def on_done(self):
        self._print('==== Leds : on_done')

    #############
    # LED STUFF #
    #############

    async def set_discoverable_effect(self, on: bool):
        self._print('set_discoverable_effect()')
        if on:
            await self.writeline('discoverable_on')
        else:
            await self.writeline('discoverable_off')
        
    async def led_strobe_on(self):
        self._print('led_strobe_on()')
        await self.writeline(
            'strobe\n'
            '{}'.format(DEFAULT_STROBE_VALUE)
        )

    async def led_strobe_off(self):
        self._print('led_strobe_off()')
        await self.writeline('strobe_off')
        # await self._wait_ack('strobe_off_ack')
        # await self._wait_ack('strobe_off_ok')
    
    async def is_strobe_on(self):
        """
        Waits for a result from `on_strobe_on()`
        """
        self._print('is_strobe_on')
        with self._strobe_on_lock:
            self._strobe_on_future = concurrent.futures.Future[bool]()
            await self.writeline('is_strobe_on')
            strobe_on = self._strobe_on_future.result()
            self._strobe_on_future = None
            return strobe_on
    
    async def on_strobe_on(self):
        """
        Notifies the waiter in `is_strobe_on()`
        """
        if self._strobe_on_future is None:
            # is_strobe_on() is not waiting for the value so discard it.
            return
        try:
            strobe_on = bool(int(await self.readline()))
            self._print(f'strobe_on: {strobe_on}')
            self._strobe_on_future.set_result(strobe_on)
        except Exception as e:
            self._strobe_on_future.set_exception(e)
    
    async def on_no_on_handler(self):
        line = await self.readline()
        self._print('no on handler: {}'.format(line))
    

    async def on_strobe_ack(self):
        self._print('on_strobe_ack')
        # Next line should be an example of how the value is expected
        # to be formatted.
        await self.readline()
    
    def no_on_handler(self, on_command, err):
        self._print('no_on_handler: {}\n{}'.format(on_command, err))
    
    async def add_led_effect(self, effect_string: str):
        """
        effect_string: 
            formatted as:
                [effect] [brightness] [r] [g] [b]
        """
        await self.writeline(f'set_effect\n{effect_string}')


class TestParent(ParentProcess):
    def __init__(self, leds_proc: LedsChildProcess):
        self.leds_proc = leds_proc
    
    async def on_led_strobe_on(self):
        self.writeline('on_led_strobe_on')
        await self.leds_proc.led_strobe_on()
    
    async def on_led_strobe_off(self):
        self.writeline('on_led_strobe_off')
        await self.leds_proc.led_strobe_off()
    
    async def on_discoverable(self):
        """
        The handler for when bluetooth changes its discoverability to other devices.
        """
        line = await self.readline()
        if line == '1':
            await self.leds_proc.set_discoverable_effect(True)
        elif line == '0':
            await self.leds_proc.set_discoverable_effect(False)
    

# Run to test.
if __name__ == '__main__':
    leds_proc = LedsChildProcess()
    parent = TestParent(leds_proc)
    processes: list = [
        parent,
        leds_proc
    ]
    futures = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # We create a thread for each to-be-executed child process
        # so that asyncio manages one child process per thread.
        for process in processes:
            futures.append(executor.submit(asyncio.run, process.begin()))
    print(len(futures))
    concurrent.futures.wait(futures)