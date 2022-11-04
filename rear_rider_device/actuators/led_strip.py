from dataclasses import dataclass
from threading import Condition
import time
import board
import neopixel
GPIO_PIN = board.D18
NUM_PIXELS = 16
INIT_BRIGHTNESS = 0.1

OFF_COLOR = (0,0,0)
WHITE = (255,255,255)

DEFAULT_FPS = 5
"""
10 frames per second is good for a strobe light with 5 blinks per second.
"""

MAX_BRIGHTNESS = 0.1


class LedStripController():
    def __init__(self, pixels: neopixel.NeoPixel):
        self._pixels = pixels
        self._brightness_value = INIT_BRIGHTNESS

    def _show_then_delay(self, seconds_delay: float):
        """
        Display the pixels with a delay.
        """
        self._pixels.show()
        time.sleep(seconds_delay)

    def test_rgb(self):
        def show():
            self._show_then_delay(0.5)
        pixels = self._pixels
        pixels.fill((0,0,255))
        show()
        pixels.fill((0,255,0))
        show()
        pixels.fill((255,0,0))
        show()
        pixels.fill(WHITE)
        show()
        pixels.fill(OFF_COLOR)
        show()
    
    def fill(self, colors: tuple[int,int,int]):
        """
        colors:
            Tuple order is [R, G, B].
        """
        self._pixels.fill(colors)

    def blink(self, duration: float, open_color = WHITE, closed_color = OFF_COLOR):
        """
        frequency:
            - In Hz
            - "per second"
        duration:
            - in seconds for each half of the blink
                - half closing
                - half closed
        
        in total total_duration = 2*duration
        """
        pixels = self._pixels
        pixels.fill(open_color)
        self._show_then_delay(duration)
        pixels.fill(closed_color)
        self._show_then_delay(duration)
    
    def strobe_stop(self):
        # print('stop strobing')
        pass

    def turn_off(self):
        self._pixels.brightness = 0
        self._pixels.show()
    
    def turn_on(self):
        self.set_brightness(self._brightness_value)
    
    def set_brightness(self, value: float):
        """
        0.0 - 1.0, but is limited to MAX_BRIGHTNESS which scales the brightness additionaly from 0.0 - 1.0
        """
        self._pixels.brightness = self._brightness_value = value * MAX_BRIGHTNESS
        self._pixels.show()
    
    def show(self):
        self._pixels.show()
    
    def set(self, index: int, color: tuple[int, int, int]):
        self._pixels[index] = color
        

def create_neopixel():
    return neopixel.NeoPixel(GPIO_PIN, NUM_PIXELS, brightness=INIT_BRIGHTNESS)
    

@dataclass
class LedStripFrame():
    """
    A from of the led strip at one point in time.
    """
    fps: int
    frame_num: int = -1
    start_time: int = 0
    end_time: int = 0
    time_elapsed: int = 0

class LedStripEffect():
    """
    Using
    """
    def affect(self, frame: LedStripFrame, led_strip_con: LedStripController):
        """
        An inheriting class can control what the effect looks like at the given frame.
        This should happen as fast as possible as it is akin to generating a signal.
        """
        raise NotImplementedError('LightStripEffect.show() is not implemented yet!')

    def new_frame(self, frame: LedStripFrame):
        """
        An inheriting class should do any calculations here for the `affect` phase.
        """
        raise NotImplementedError('')

class StrobeEffect(LedStripEffect):
    """
    Blinks at a frequency matching the frame's fps.
    """
    def __init__(self, color: tuple[int, int, int] = WHITE):
        self._color = color

    def affect(self, frame: LedStripFrame, led_strip_con: LedStripController):
        led_strip_con.fill(self._curr_color)

    def new_frame(self, frame: LedStripFrame):
        if frame.frame_num % 2 == 0:
            self._curr_color = self._color
        else:
            self._curr_color = OFF_COLOR


class LedsEffectsLoopContext:
    def __init__(self, led_strip_ctrl: LedStripController, frame: LedStripFrame):
        self._effects: list[LedStripEffect] = []
        self._frame = frame
        self._led_strip_ctrl = led_strip_ctrl
        self._loop = True
        """
        Used by a while loop to determine if the loop should continue to the next iteration.
        """
        self._play = False
        self.play_condition = Condition()
    
    def get_loop_vars(self):
        return (self._led_strip_ctrl, self._effects, self._frame)
    
    def update_elapsed_time(self):
        self._frame.time_elapsed = self._frame.end_time - self._frame.start_time

    def set_effects(self, effects: list[LedStripEffect]):
        with self.play_condition:
            self._effects = effects
            self.play_condition.notify()
    
    ###
    # Control the loop.
    ###

    def continue_loop(self):
        return self._loop
    
    def should_play(self):
        """
        Determine if the the effects should be playing.
        """
        return self._play and len(self._effects) > 0
    
    def play(self):
        """
        Play the effects.
        """
        self._play = True

    def pause(self):
        """
        Pause the effects.
        """
        self._play = False

    def stop(self):
        """
        Stop the effects by marking the loop as done.
        """
        with self.play_condition:
            self._loop = False
            self._play = False
            self.play_condition.notify()


def enter_leds_effects_loop(loop_ctx: LedsEffectsLoopContext):
    def effects_too_slow():
        # print('!!! The effects are too slow for the framerate !!!')
        pass
    def update_elapsed_time():
        loop_ctx.update_elapsed_time()
        
    while loop_ctx.continue_loop():
        with loop_ctx.play_condition:
            while (loop_ctx.should_play() is False) and (loop_ctx.continue_loop() is True):
                loop_ctx.play_condition.wait()
            if loop_ctx.continue_loop() is False:
                break
            led_strip, effects, frame = loop_ctx.get_loop_vars()
            frame.frame_num += 1
            frame.start_time = time.time_ns()
            for effect in effects:
                effect.new_frame(frame)
            for effect in effects:
                effect.affect(frame, led_strip_con=led_strip)
            frame.end_time = time.time_ns()
            update_elapsed_time()
            frame_duration = 1.0/frame.fps
            time_to_sleep = frame_duration - frame.time_elapsed / 1_000_000_000.0
            if time_to_sleep < 0:
                effects_too_slow()
                continue
        time.sleep(time_to_sleep)
        led_strip.show()
        # print('slept for {} second(s).'.format(time_to_sleep))


if __name__ == '__main__':
    pixels = create_neopixel()
    led_strip = LedStripController(pixels)
    # TODO add an Effect that selects leds in a group to apply an effect to. Effect mask?
    try:
        loop_ctx = LedsEffectsLoopContext(
            led_strip_ctrl=led_strip,
            frame=LedStripFrame(fps=DEFAULT_FPS))
        loop_ctx.set_effects([StrobeEffect()])
        enter_leds_effects_loop(loop_ctx)
    finally:
        print('turning off')
        led_strip.turn_off()
        pixels.deinit()

