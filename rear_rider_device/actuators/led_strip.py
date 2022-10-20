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

    def strobe(self, frequency: int, duration: float):
        """
        frequency:
            - In Hz
            - "per second"
        duration:
            - in seconds
        """
        sleep_seconds = (1/frequency) / 2
        pixels = self._pixels
        num_flashes = int(frequency * duration)
        print('Number of flashes: {}'.format(num_flashes))
        for i in range(num_flashes):
            pixels.fill(WHITE)
            self._show_then_delay(sleep_seconds)
            pixels.fill((0,0,0))
            self._show_then_delay(sleep_seconds)

    def turn_off(self):
        pixels = self._pixels
        pixels.fill(OFF_COLOR)
        pixels.show()
    
    def turn_on(self):
        self._pixels.show()

def create_neopixel():
    return neopixel.NeoPixel(GPIO_PIN, NUM_PIXELS, brightness=INIT_BRIGHTNESS)

if __name__ == '__main__':
    pixels = create_neopixel()
    led_strip = LedStripController(pixels)
    try:
        while True:
            led_strip.test_rgb()
            led_strip.strobe(2, 16)
            # led_strip.turn_on()
    except KeyboardInterrupt:
        pass
    led_strip.turn_off()
    pixels.deinit()
