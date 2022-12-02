import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(
                os.path.dirname(__file__),
                # This file should be in `rear_rider_device/` so we need to travel up one directory.
                f'{os.pardir}')
)
sys.path.append(PROJECT_ROOT)

import asyncio
from pkgutil import get_data
import readline
from sys import stdout
from rear_rider_device.ipc.parent_process import ParentProcess
import rear_rider_device.rear_rider_sensors.camera as camera
import os
from datetime import datetime
from datetime import date

class CameraParentProcess(ParentProcess):
    def __init__(self, camera: camera.RRCamera):
        self.camera = camera

    async def pre_ready(self):
        pass
    def pre_done(self):
        pass
    def no_ack(self):
        pass
    def no_on_handler(self):
        pass

    async def on_get_picture(self):
        self.camera.takePhoto()
    async def on_get_stream(self):
        self.camera.beginStream()
    async def on_get_recording(self):
        self.camera.startRec()
    async def on_end_stream(self):
        self.camera.endStream()
    async def on_help(self):
        self.writeline(">get_picture: takes a photo via the camera and saves it.\n\t-no parameters needed.\n" + 
                       ">get_stream: starts up the stream and which can be monitored on 'localhost:8000'. \n\t-no parameters neeeded\n" + 
                       ">get_recording: starts a recording that lasts for a {} seconds.\n\t-no parameters needed.\n".format(self.camera.DEF_VLEN))
if __name__ == '__main__':
    cam = camera.RRCamera()
    camera_parent_proc = CameraParentProcess(camera=cam)
    #Begin session with the parent process. The parent process is collecting the data.
    asyncio.run(camera_parent_proc.begin())
