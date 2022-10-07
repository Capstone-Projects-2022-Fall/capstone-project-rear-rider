from picamera import PiCamera
from time import sleep
from datetime import datetime
from datetime import date

now = datetime.now()
today = date.today()
current_time = str(now.strftime("%H:%M:%S"))
current_date = str(today.strftime('%Y-%m-%d'))
print("Current Time = " + current_time)
print("Current Date = " + current_date)

photo_name = "image at " + current_time + " on "+ current_date +".jpg"
vid_name = "vid at " + current_time + " on "+ current_date + ".h264"

camera = PiCamera()
camera.start_preview()
camera.capture(photo_name)
camera.stop_preview()
camera.start_preview()
camera.start_recording(vid_name)
camera.wait_recording(5)
camera.stop_recording()
camera.stop_preview()