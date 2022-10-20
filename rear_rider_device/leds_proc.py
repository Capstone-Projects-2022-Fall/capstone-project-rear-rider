import asyncio
from sys import path
from typing import Union
from ipc.parent_process import ParentProcess
from actuators.led_strip import LedStripController, create_neopixel

path.append("rear_rider_bluetooth_server/src/")

WHITE = (255, 255, 255)

class LedsParentProcess(ParentProcess):
    """
    The parent process of the leds process.
    """
    def __init__(self, led_strip: LedStripController):
        self.led_strip = led_strip
    
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
        """
        params_line = await self.readline()

        try:    
            params = params_line.split(' ')
            self.led_strip.strobe(int(params[0]), float(params[1]))
        except Exception:
            pass
    
    async def on_set_brightness(self):
        """
        Expects:
            One line that is parsed as a float value from 0.0 to 1.0.

            Formatted like:
                `"{}\n".format(brightness)`
        """
        brightness_value_line = await self.readline()

        try:
            self.led_strip._pixels.brightness = float(brightness_value_line)
            self.led_strip._pixels.show()
        except Exception:
            pass
    
    async def on_help(self):
        def help_command_param(param: str, description: str, example: str):
            return (
                '           {} - {}\n'
                '               e.g.:\n'
                '                   {}\n'.format(
                    param, description, example
                ))
        def help_command(command: str, description: str, params: list[tuple[str,str,str]]):
            
            params_help_str = ''
            self.writeline('test')
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
            self.writeline('test0')
            # return 
            help_commands_str += '{}\n'.format(help_command(
                _help_command[0], _help_command[1], _help_command[2]))
        self.writeline(
            'Commands:\n'
            '{}'.format(help_commands_str)
        )
    
    def pre_done(self):
        self.led_strip.turn_off()


if __name__ == '__main__':
    pixels = create_neopixel()
    led_strip = LedStripController(pixels)
    leds_parent_process = LedsParentProcess(led_strip)
    asyncio.run(leds_parent_process.begin())
    pixels.deinit()