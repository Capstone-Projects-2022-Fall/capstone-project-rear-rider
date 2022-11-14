from rear_rider_device.leds_child_proc import LedsChildProcess
import unittest
import threading
import asyncio

class ManualTestLedsChildProcess(unittest.IsolatedAsyncioTestCase):
    """
    Perform a manual test on the `LedsChildProcess` class.

    These test cases will ask you to type in "Y" or "y" to confirm that a test passed.
    """
    def setUp(self) -> None:
        self._leds_child_process = LedsChildProcess()
        self._leds_thread = threading.Thread(target=asyncio.run,
                args=(self._leds_child_process.begin(),))
        self._leds_thread.start()
        self._leds_child_process.wait_ready()
    
    async def asyncSetUp(self) -> None:
        pass

    async def asyncTearDown(self) -> None:
        await self._leds_child_process.exit()

    def tearDown(self) -> None:
        self._leds_thread.join()
    
    def assertTypeYToPass(self, prompt: str):
        '''
        Assert if "Y" or "y" are not provided as input.
        '''
        res = input(f'{prompt}\n\nType "Y" to confirm> ')
        self.assertEqual('y', res.lower(),
            msg='"Y" or "y" was not input. Assuming the test case failed.')

    async def test_set_discoverable_effect(self):
        '''
        Set the discoverable effect on, then turn it off.
        '''
        await self._leds_child_process.set_discoverable_effect(True)
        self.assertTypeYToPass('Is the discoverable effect on?')

        await self._leds_child_process.set_discoverable_effect(False)
        self.assertTypeYToPass('Is the discoverable effect off?')
    
    async def test_is_strobe_on(self):
        '''
        Return true if the strobe light is on.
        '''
        await self._leds_child_process.led_strobe_on()
        await self._leds_child_process.is_strobe_on()
        self.assertTypeYToPass('Is the strobe light on and does the line above read "True"?')

        await self._leds_child_process.led_strobe_off()
        await self._leds_child_process.is_strobe_on()
        self.assertTypeYToPass('Is the strobe light off and does the line above read "False"?')

    def test_add_led_effect(self):
        '''
        Adding a strobe effect.
        '''
        raise NotImplementedError('test_add_led_effect')

def test_cases():
    return [
        ManualTestLedsChildProcess('test_set_discoverable_effect'),
        ManualTestLedsChildProcess('test_is_strobe_on'),
        # ManualTestLedsChildProcess('test_add_led_effect')
    ]
