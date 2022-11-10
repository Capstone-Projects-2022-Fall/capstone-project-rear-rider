import unittest
import rear_rider_sensors.camera as camera
import socket
from time import sleep
from unittest import IsolatedAsyncioTestCase

class AsyncCameraUnitTest(IsolatedAsyncioTestCase):
    
    cam : camera.RRCamera = None

    async def test_beginstream(self):
        port = 8000
        self.cam.beginStream()
        sleep(5) #needed to let the stream boot up
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self.assertTrue(s.connect_ex(('localhost', port)) == 0)
        self.cam.endStream() #need to manually end the stream

    async def test_endstream(self):
        port = 8000
        self.cam.beginStream()
        sleep(5) #needed to let the stream boot up
        self.cam.endStream() #need to manually end the stream
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self.assertFalse(s.connect_ex(('localhost', port)) == 0)

if __name__ == '__main__':
    AsyncCameraUnitTest.cam = camera.RRCamera()
    unittest.main()