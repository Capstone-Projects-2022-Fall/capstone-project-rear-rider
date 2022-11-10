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

    DEF_VLEN = 15
    def __init__(self):
        self.pc = Picamera2()
        self.media_loc = os.path.dirname(__file__) + "/../media_storage/"
        self._stream_thread: Union[None, Thread] = None
        self._stream_server: Union[None, StreamingServer] = None

    def takePhoto(self, photoName = "image_at_"    + current_time + "_on_" + current_date):
        photoLocation = self.media_loc + photoName + ".jpg"
        self.pc.start() 
        self.pc.capture_file(photoLocation)
        self.pc.stop();

    def startRec(self, videoName = "video_at_" + current_time + "_on_" + current_date):  # I had to change the spaces to _ because of ffmjepg using spaces as delimters and 
        videoLocation = self.media_loc + videoName + ".mp4"                              # that made the conversion of the file to bug and break.
        self.pc.start_and_record_video(output = videoLocation, duration = self.DEF_VLEN)

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
