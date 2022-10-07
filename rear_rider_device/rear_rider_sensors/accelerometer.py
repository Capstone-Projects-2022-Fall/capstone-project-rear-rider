import asyncio
import board
import busio
import adafruit_adxl34x

i2c = busio.I2C(board.SCL, board.SDA)

class Accelerometer():
    def __init__(self):
        """
        Get the attached accelerometer.
        """
        accelerometer = adafruit_adxl34x.ADXL345(i2c)
        accelerometer.enable_freefall_detection(threshold=10, time=25)
        accelerometer.enable_motion_detection(threshold=18)
        accelerometer.enable_tap_detection(tap_count=1, threshold=20, duration=50, latency=20, window=255)
        self.accelerometer = accelerometer

    def get_acceleration(self):
        """
        Get the current acceleration vector.
        """
        return self.accelerometer.acceleration

    def get_freefall(self):
        return self.accelerometer.events['freefall']

    def get_tapped(self):
        return self.accelerometer.events['tap']

    def get_motion(self):
        return self.accelerometer.events['motion']


if __name__ == '__main__':
    accelerometer = Accelerometer()
    while True:
        print('%f %f %f'%accelerometer.get_acceleration())
