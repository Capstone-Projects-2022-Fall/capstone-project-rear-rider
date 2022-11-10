import unittest
import rear_rider_sensors.camera as camera
import os

class CameraUnitTest(unittest.TestCase):

    cam : camera.RRCamera = None

    def test_picture(self):
        pic_name = "PhotoUnitTest"
        self.cam.takePhoto(pic_name)
        file_exists = os.path.exists(os.path.dirname(__file__) + "/media_storage/" + pic_name + '.jpg')
        self.assertTrue(file_exists)

    def test_recording(self):
        vid_name = "VideoUnitTest"
        self.cam.startRec(vid_name)
        file_exists = os.path.exists(os.path.dirname(__file__) + "/media_storage/" + vid_name + '.mp4')
        self.assertTrue(file_exists)

if __name__ == '__main__':
    CameraUnitTest.cam = camera.RRCamera()
    unittest.main()