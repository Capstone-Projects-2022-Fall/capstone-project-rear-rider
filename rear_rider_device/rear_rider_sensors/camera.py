from threading import Thread
from typing import Union
from picamera2 import Picamera2
from datetime import datetime
from datetime import date
import os

from rear_rider_sensors.camera_stream import StreamingServer, begin_stream

class RRMedia:
    def __init__(self):
        self.media_id

class RRCamera:

    now = datetime.now()
    today = date.today()
    current_time = str(now.strftime("%H:%M:%S"))
    current_date = str(today.strftime('%Y-%m-%d'))

    defaultPhotoName = "image at "    + current_time + " on " + current_date + ".jpg"
    defaultVideoName = "orig vid at " + current_time + " on " + current_date + ".h264"

    def __init__(self, storage_path = os.path.dirname(__file__) + "/", name = defaultPhotoName):
        self.pc = Picamera2()
        self.media_loc = storage_path + name
        self.def_vid_len = 10
        self.def_loc = storage_path
        self._stream_thread: Union[None, Thread] = None
        self._stream_server: Union[None, StreamingServer] = None

    def takePhoto(self, photoName):
        photoLocation = self.def_loc + photoName
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", photoLocation)
        self.pc.start() 
        self.pc.capture_file(photoLocation)
        self.pc.stop();

    def startRec(self, videoName, videoLen):
        videoLocation = self.def_loc + videoName
        self.pc.start_and_record_video(videoLocation, duration = videoLen)

    def beginStream(self):
        def on_stream_server(stream_server: StreamingServer):
            self._stream_server = stream_server
        if self._is_streaming():
            return
        self._stream_thread = Thread(target=begin_stream,
                args=(self.pc, on_stream_server,))
        self._stream_thread.start()


    def endStream(self):
        if self._is_streaming():
            # Close the server so that the port can be reused.
            self._stream_server.server_close()
            # Stop serving the stream to clients.
            self._stream_server.shutdown()
            # Don't leave an unjoined thread.
            self._stream_thread.join()
            self._stream_server = None
            self._stream_thread = None
    
    def _is_streaming(self):
        return self._stream_thread is not None

    def DefMediaName(media_type : str):
        now = datetime.now()
        today = date.today()
        current_time = str(now.strftime("%H:%M:%S"))
        current_date = str(today.strftime('%Y-%m-%d'))
        name = str(datetime.now().strftime("%H:%M:%S")) + " on " + str(date.today().strftime('%Y-%m-%d'))
        if media_type == 'vid':
            return "vid at " + current_time + " on " + current_date + ".h264"
        elif media_type == 'pic':
            return "image at "    + current_time + " on " + current_date + ".jpg"