import math
import time
import unittest
from unittest import IsolatedAsyncioTestCase
import sys
sys.path.append("../rear_rider_device")
from actuators.led_strip import LedStripController, create_neopixel


class TestLEDStrip(unittest.IsolatedAsyncioTestCase):
    
    pixels = create_neopixel()
    led_strip = LedStripController(pixels)
    
    async def test_set_brightness(self):
        '''
        Using a default brightness of 0.70 and the brightness calculator of 
        BRIGHTNESS*0.1, the brightness is set with set_brightness() and then checked against the formula.
        '''
        BRIGHTNESS = 0.70
        self.led_strip.set_brightness(BRIGHTNESS)
        self.assertTrue(self.led_strip._brightness_value == BRIGHTNESS*0.1) #.1 Comes from MAX_BRIGHTNESS value specified in led_strip.py
        
    async def test_fill(self):
        '''
        Using Red as 255,0,0 this test uses fill() to set the 
        color of the lights and then check the pixels of the light strip for their RGB value
        '''
        RED = [255,0,0]
        self.led_strip.fill(RED)
        self.assertTrue(RED==self.led_strip._pixels._getitem(1))
        
    async def test_blink(self):
        '''
        Since blink() uses a two bursts of the duration param to change the lights, this test 
        uses a DURATION of 5 and records the time before and after call to blink(). 
        if the difference of the two times matches DURATION*2 then it works
        '''
        DURATION = 5
        begin = time.perf_counter()
        self.led_strip.blink(duration = DURATION)
        end = time.perf_counter()
        tot_time = math.floor(end - begin)
        self.assertTrue(tot_time == DURATION*2)
        
    async def test_turn_on(self):
        '''
        turn_on() sets the brigness of the strip to _brightness_value so this 
        test checks _brightness_value after a call to turn_on()
        '''
        self.led_strip.turn_on()
        self.assertTrue(self.led_strip._brightness_value == self.led_strip._brightness_value)
    
    async def test_turn_off(self):
        '''
        turn_off sets the brightness of the strip to zero so this test 
        checks the value of the strip's _pixles.brighness value and if it matches zero
        '''
        self.led_strip.turn_off()
        self.assertTrue(self.led_strip._pixels.brightness == 0)
    
def test_cases():
    return [
        TestLEDStrip('test_set_brightness'),
        TestLEDStrip('test_fill'),
        TestLEDStrip('test_blink'),
        TestLEDStrip('test_turn_on'),
        TestLEDStrip('test_turn_off')
    ]