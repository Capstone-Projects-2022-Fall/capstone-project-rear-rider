import time
import board
import neopixel
GPIO_PIN = board.D18
NUM_PIXELS = 16
INIT_BRIGHTNESS = 0.008

OFF_COLOR = (0,0,0)
WHITE = (255,255,255)

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
        0.0 - 1.0
        """
        self._pixels.brightness = self._brightness_value = value
        self._pixels.show()
    
    def show(self):
        self._pixels.show()
        

def create_neopixel():
    return neopixel.NeoPixel(GPIO_PIN, NUM_PIXELS, brightness=INIT_BRIGHTNESS)


if __name__ == '__main__':
    pixels = create_neopixel()
    led_strip = LedStripController(pixels)
    try:
        while True:
            # led_strip.test_rgb()
            # led_strip.strobe(2, 16)
            led_strip._pixels.brightness = 0.1
            led_strip._pixels[0] = (255, 0, 0)
            led_strip._show_then_delay(1)
            led_strip._pixels[1] = (0, 255, 0)
            led_strip._show_then_delay(1)
            led_strip._pixels[2] = (0, 0, 255)
            led_strip._show_then_delay(1)
            led_strip._pixels[0] = (0, 0, 0)
            led_strip._show_then_delay(1)
            led_strip.fill((0,0,0))
            led_strip._show_then_delay(1)
            # led_strip.turn_on()
    except KeyboardInterrupt:
        pass
    led_strip.turn_off()
    pixels.deinit()
