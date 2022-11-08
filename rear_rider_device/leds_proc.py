import asyncio
from sys import path
from threading import Thread
from typing import Union
from ipc.parent_process import ParentProcess
from actuators.led_strip import BlankEffect, LedStripController, LedStripFrame, LedsEffectsLoopContext, StrobeEffect, create_neopixel, enter_leds_effects_loop

path.append("rear_rider_bluetooth_server/src/")

WHITE = (255, 255, 255)
OFF_COLOR = (0,0,0)
DISCOVERABLE_EFFECT_COLOR = (0, 128, 255)
STROBE_TASK_FUTURE_WAIT_TIME = 0.1
"""
In seconds
"""

class LedsParentProcess(ParentProcess):
    """
    The parent process of the leds process.
    """
    _leds_effects_loop_thread: Union[None, Thread]
    def __init__(self, led_strip: LedStripController):
        self.led_strip = led_strip
        self._strobe_on = False
        self._leds_effects_loop_thread = None
        self._leds_effects_loop_ctx = LedsEffectsLoopContext(self.led_strip, frame=LedStripFrame(5))
    
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
        params = params_line.split(' ')
        frequency = int(params[0])
        # duration = float(params[1])
        self._set_strobe_effect(frequency, WHITE)

    async def pre_ready(self):
        if self._leds_effects_loop_thread is not None:
            raise Exception('_strobe_task_thread should be `None`')
        self._leds_effects_loop_thread = Thread(
            target=enter_leds_effects_loop,
            name='leds_effects_loop',
            args=(self._leds_effects_loop_ctx,))
        self._leds_effects_loop_thread.start()
        self._leds_effects_loop_ctx.play()
    
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
        self._join_leds_thread()
        self.led_strip.turn_off()
    
    def no_on_handler(self, on_command: str, err: Exception):
        self.writeline(
            'no_on_handler\n'
            '>> {} << {}'.format(on_command, err)
        )
    
    async def on_is_strobe_on(self):
        self.writeline(
            'strobe_on\n'
            '{}'.format(self._strobe_on)
        )
    
    async def on_strobe_off(self):
        self._leds_effects_loop_ctx.set_effects([BlankEffect()])
        self._leds_effects_loop_ctx.play()
    
    def _join_leds_thread(self):
        if self._leds_effects_loop_thread is not None:
            self._leds_effects_loop_ctx.stop()
            self._leds_effects_loop_thread.join()
            self._leds_effects_loop_thread = None
    
    async def on_discoverable_on(self):
        self.led_strip.set_brightness(0.25)
        self._set_strobe_effect(1, DISCOVERABLE_EFFECT_COLOR)

    async def on_discoverable_off(self):
        self._leds_effects_loop_ctx.set_effects([])
        self.led_strip.turn_off()
    
    async def on_set_effect(self):
        params = (await self.readline()).split(' ')
        pattern = params[0]
        brightness = params[1]
        """brightness
        1 - low
        2 - medium
        3 - high
        """
        color = (int(params[2]), int(params[3]), int(params[4]))
        if pattern != '1':
            # Since '1' defines the only pattern implemented we should return early if pattern is not '1'
            return
        self.led_strip.set_brightness(1.0 / (4 - int(brightness)))
        self._set_strobe_effect(5, color)
        self._leds_effects_loop_ctx.play()
    
    def _set_strobe_effect(self, frequency, color):
        self._leds_effects_loop_ctx._frame.fps = frequency
        self._leds_effects_loop_ctx.set_effects([StrobeEffect(color=color)])
    
    async def on_effects_pause(self):
        self._leds_effects_loop_ctx.pause()
    
    async def on_effects_play(self):
        with self._leds_effects_loop_ctx.play_condition:
            self._leds_effects_loop_ctx.play()
            self._leds_effects_loop_ctx.play_condition.notify()

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

help_str_all += '{}\nhelp_string_end'.format(help_commands_section_str)

if __name__ == '__main__':
    pixels = create_neopixel()
    led_strip = LedStripController(pixels)
    leds_parent_process = LedsParentProcess(led_strip)
    async def main():
        try:
            await leds_parent_process.begin()
        except:
            print('unexpected error')
        finally:
            pixels.deinit()
        
    asyncio.run(main())