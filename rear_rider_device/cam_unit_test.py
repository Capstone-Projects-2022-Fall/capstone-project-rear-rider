import unittest
import rear_rider_sensors.camera as camera
import os

class CameraUnitTest(unittest.TestCase):

    cam : camera.RRCamera = None

    def test_picture(self):
        '''Tests the photo capability of the camera by creating a photo
         with takePhoto() and assert that the file exists after'''
        pic_name = "PhotoUnitTest"
        self.cam.takePhoto(pic_name)
        file_exists = os.path.exists(os.path.dirname(__file__) + "/media_storage/" + pic_name + '.jpg')
        self.assertTrue(file_exists)

    def test_recording(self):
        '''Tests the video capability of the camera by creating a video 
        with startRec(name, duration) and assert it exists in the correct location'''
        vid_name = "VideoUnitTest"
        self.cam.startRec(vid_name, vidLen=2)
        file_exists = os.path.exists(os.path.dirname(__file__) + "/media_storage/" + vid_name + '.mp4')
        self.assertTrue(file_exists)

if __name__ == '__main__':
    CameraUnitTest.cam = camera.RRCamera()
    unittest.main()