import asyncio
import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(
                os.path.dirname(__file__),
                # This file should be in `rear_rider_device/` so we need to travel up one directory.
                f'{os.pardir}')
)
sys.path.append(PROJECT_ROOT)

from rear_rider_device.ipc.parent_process import ParentProcess
import rear_rider_device.rear_rider_sensors.lidar as lidar

class LidarParentProcess(ParentProcess):
    def __init__(self, lidar: lidar.Lidar):
        self.lidar = lidar

    async def pre_ready(self):
        pass

    def pre_done(self):
        pass
    
    def no_ack(self):
        pass
    
    def no_on_handler(self):
        pass

    async def on_get_data(self):
        lidar = self.lidar
        distance , strength = lidar.getTFminiData()
        data = ("data\n" f"{distance} {strength}")
        self.writeline(data)
    
    async def on_send_picture_signal(self):
        # not sure what to do here
        picture_signal = 'picture_signal'
        self.writeline(picture_signal)

if __name__ == '__main__':
    lidar = lidar.Lidar()
    lidar_parent_proc = LidarParentProcess(lidar=lidar)
    # Begin session with the parent process. The parent process is collecting the data.
    asyncio.run(lidar_parent_proc.begin())
