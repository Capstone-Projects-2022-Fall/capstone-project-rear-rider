
import io
import logging
import socketserver
from http import server
from threading import Condition, Thread
from typing import Callable

from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

class StreamingHandler(server.BaseHTTPRequestHandler):
    def __init__(self, request: bytes, client_address: tuple[str, int], server: socketserver.BaseServer,
            output: StreamingOutput) -> None:
        # https://stackoverflow.com/a/62349797
        self._output = output
        super().__init__(request, client_address, server)
    def do_GET(self):
        if self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                output = self._output
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

def begin_stream(pi_camera: Picamera2, on_stream_server: Callable[[StreamingServer],None]):
    output = StreamingOutput()
    pi_camera.configure(pi_camera.create_video_configuration(main={"size": (640, 480)}))  # type: ignore
    pi_camera.start_recording(JpegEncoder(), FileOutput(output))
    def get_streaming_handler(x, y, z):
        return StreamingHandler(x, y, z, output=output)
    try:
        address = ('', 8000)
        stream_server = StreamingServer(address, get_streaming_handler)
        on_stream_server(stream_server)
        stream_server.serve_forever()
    finally:
        pi_camera.stop_recording()