import asyncio
from pkgutil import get_data
import readline
from sys import stdout
from ipc.parent_process import ParentProcess
import rear_rider_sensors.camera as camera
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

    async def on_get_picture(self, name = str(datetime.now().strftime("%H:%M:%S")) + " on " + str(date.today().strftime('%Y-%m-%d'))):
        self.camera.takePhoto(name + ".jpg")
        #await self.writeline('on_picture')
    async def on_get_stream(self):
        self.camera.beginStream()
    async def on_get_recording(self):
        self.camera.startRec("IPC_RECORDING_TEST.mp4", 15)
    async def on_end_stream(self):
        self.camera.endStream()
    async def on_help(self):
        self.writeline(">get_picture: takes a photo via the camera and saves it.\n\t-no parameters needed, but you can specify a name if needed.\n" + 
                       ">get_stream: starts up the stream and which can be monitored on 'localhost:8000'. \n\t-no parameters neeeded\n" + 
                       ">get_recording: starts a recording that lasts for a 10 seconds.\n\t-no parameters needed, but you can specify a name if needed.\n")
if __name__ == '__main__':
    cam = camera.RRCamera()
    camera_parent_proc = CameraParentProcess(camera=cam)
    #Begin session with the parent process. The parent process is collecting the data.
    asyncio.run(camera_parent_proc.begin())
