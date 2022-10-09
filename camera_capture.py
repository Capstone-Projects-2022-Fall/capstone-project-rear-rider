from picamera2 import Picamera2, Preview
from time import sleep
from datetime import datetime
from datetime import date
import os
from videoprops import get_video_properties

now = datetime.now()
today = date.today()
current_time = str(now.strftime("%H:%M:%S"))
current_date = str(today.strftime('%Y-%m-%d'))
print("Current Time = " + current_time)
print("Current Date = " + current_date)

runtime_path = os.path.dirname(__file__) + "/"

photo_name = runtime_path + "image at "    + current_time + " on " + current_date + ".jpg"
vid_name = runtime_path   + "orig vid at " + current_time + " on " + current_date + ".h264"


picam2 = Picamera2() 
#camera_config = picam2.create_preview_configuration() 
#picam2.configure(camera_config) 
picam2.start() 
sleep(2) 
picam2.capture_file(photo_name)
props = get_video_properties(photo_name)
print(photo_name + ">>>>>>>>>>>" + str(props['width']) + "x" + str(props["height"]))

picam2.start_and_record_video(vid_name, duration = 10)
props = get_video_properties(vid_name)
print(photo_name + ">>>>>>>>>>>" + str(props['width']) + "x" + str(props["height"]) + "\n frames: " + str(props["avg_frame_rate"]))
