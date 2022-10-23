import asyncio
from concurrent.futures import ThreadPoolExecutor
import readline
from sys import path
from typing import Union
from ipc.parent_process import ParentProcess
from actuators.led_strip import LedStripController, create_neopixel

path.append("rear_rider_bluetooth_server/src/")

WHITE = (255, 255, 255)
OFF_COLOR = (0,0,0)
STROBE_TASK_FUTURE_WAIT_TIME = 0
"""
In seconds
"""

class LedsParentProcess(ParentProcess):
    """
    The parent process of the leds process.
    """
    _strobe_task_future: Union[None, asyncio.Task]
    def __init__(self, led_strip: LedStripController):
        self.led_strip = led_strip
        self._strobe_on = False
        self._strobe_task_future = None
    
    async def on_turn_on(self):
        """
        Expects:
            
        """
        color_value_line = await self.readline()
        
        try:
            color_value_split = color_value_line.split(' ')
            if len(color_value_split) != 3:
                raise Exception('Color value was not 3 values long.')
            color = (int(color_value_split[0]),
                        int(color_value_split[1]),
                        int(color_value_split[2]))
            self.led_strip.fill(color)
        except Exception:
            self.led_strip.fill(WHITE)
        self.led_strip.turn_on()
        
    async def on_turn_off(self):
        self.led_strip.turn_off()
    
    async def on_strobe(self):
        """
        Expects:
            One line that contains an integer followed by a space followed by a float.

            Formatted like:
                `"{} {}\n".format(frequency, duration)`
        Ignores:
            Any requests if the leds are currently strobing.
        """
        self.writeline('strobe_ack\nFormat: [frequency] [duration]')
        params_line = await self.readline()

        if self._strobe_task_future is not None:
            # TODO: Evaluate possible race condition here.
            try:
                self.writeline('strobe_task_waiting')
                await self._wait_ack('debug_ack')
                await asyncio.tasks.wait_for(
                        asyncio.tasks.shield(self._strobe_task_future),
                        STROBE_TASK_FUTURE_WAIT_TIME)
                self._strobe_task_future = None
            except TimeoutError:
                self.writeline('strobe_on_busy')
                return
                
        def threaded_strobe_task():
            """
            Returns a coroutine 
            """
            def strobe_task():
                async def strobe():
                    try:
                        params = params_line.split(' ')
                        frequency = int(params[0])
                        duration = float(params[1])
                        self._strobe_on = True
                        sleep_seconds = (1/frequency) / 2
                        num_flashes = int(frequency * duration)
                        self.led_strip.fill(WHITE)
                        i = 0
                        while self._strobe_on and (duration == 0.0 and frequency > 0) or (i < num_flashes):
                            self.led_strip.blink(sleep_seconds,
                                open_color=WHITE,
                                closed_color=OFF_COLOR,
                            )

                            i += 1
                    except Exception as e:
                        self.writeline('strobe_error\n{}'.format(e))
                        pass
                    finally:
                        self._strobe_on = False
                asyncio.run(strobe())
            return asyncio.to_thread(strobe_task)
                
        if self._strobe_task_future is not None:
            self.writeline('strobe_on_busy')
            return
        self._strobe_task_future = asyncio.create_task(threaded_strobe_task(), name='strobe_task')
    
    async def on_set_brightness(self):
        """
        Expects:
            One line that is parsed as a float value from 0.0 to 1.0.

            Formatted like:
                `"{}\n".format(brightness)`
        """
        brightness_value_line = await self.readline()

        try:
            self.led_strip.set_brightness(float(brightness_value_line))
        except Exception:
            pass
    
    async def on_help(self):
        self.writeline(help_str_all)
    
    def pre_done(self):
        self.led_strip.turn_off()
    
    def no_on_handler(self, on_command: str, err: Exception):
        self.writeline(
            'no_on_handler\n'
            '>> {} <<'.format(on_command)
        )
    
    async def on_is_strobe_on(self):
        self.writeline(
            'strobe_on\n'
            '{}'.format(self._strobe_on)
        )
    
    async def on_strobe_off(self):
        self.writeline(
            'strobe_off_ack'
        )
        self._strobe_on = False
        self.writeline(
            'strobe_off_ok'
        )

help_str_all = ''

def help_command_param(param: str, description: str, example: str):
    return (
        '           {} - {}\n'
        '               e.g.:\n'
        '                   {}\n'.format(
            param, description, example
        ))
def help_command(command: str, description: str, params: list[tuple[str,str,str]]):
    
    params_help_str = ''
    # return
    if not (len(params) > 0):
        params_help_str += '            No parameters.'
    else:
        for param in params:
            print(len(param))
            params_help_str += '{}\n'.format(help_command_param(
                param[0], param[1], param[2]
            ))
    return (
        '   {}\n'
        '       Description:\n'
        '           {}\n'
        '       Params:\n'
        '{}'.format(
            command, description, params_help_str))
help_commands_str = ''
help_commands = [
    ('turn_on', 'Turn on the lights.', [
        ('color', '(optional) RGB values seperated by spaces.', '255 0 0')
    ]),
    ('turn_off','Turn off the lights',[
    ]),
    ('set_brightness', 'Set the brightness of the lights.', [
        ('brightness','Float value from 0.0 to 1.0.', '0.70')
    ]),
    ('strobe', 'Flash the light in a strobe like fashion', [
        ('frequency and duration', 'Frequency in Hz followed by duration in seconds.', '5 2.75')
    ])
]
for _help_command in help_commands:
    # return 
    help_commands_str += '{}\n'.format(help_command(
        _help_command[0], _help_command[1], _help_command[2]))

help_commands_section_str = (
    'Commands:\n'
    '{}'.format(help_commands_str))

help_str_all += help_commands_section_str

if __name__ == '__main__':
    pixels = create_neopixel()
    led_strip = LedStripController(pixels)
    leds_parent_process = LedsParentProcess(led_strip)
    async def main():
        try:
            await leds_parent_process.begin()
        except:
            print('unexpected error')
        
    asyncio.run(main())
    pixels.deinit()