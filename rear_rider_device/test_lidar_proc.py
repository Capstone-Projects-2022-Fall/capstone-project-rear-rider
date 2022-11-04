import asyncio
from pkgutil import get_data
from sys import stdout
from ipc.parent_process import ParentProcess
# import rear_rider_sensors.lidar as lidar

class LidarParentProcess(ParentProcess):
    def __init__(self):
        pass

    async def pre_ready(self):
        pass

    def pre_done(self):
        pass
    
    def no_ack(self):
        pass
    
    def no_on_handler(self):
        pass

    async def on_get_data(self):
        data = ("data\n" f"{14} {100}")
        self.writeline(data)

if __name__ == '__main__':
    # lidar = lidar.Lidar()
    lidar_parent_proc = LidarParentProcess()
    # Begin session with the parent process. The parent process is collecting the data.
    asyncio.run(lidar_parent_proc.begin())
