import asyncio
from ipc.parent_process import ParentProcess
import rear_rider_sensors.accelerometer as accelerometer

class AccelerometerParentProcess(ParentProcess):
    def __init__(self, accelerometer: accelerometer.Accelerometer):
        self.accelerometer = accelerometer

    async def pre_ready(self):
        pass

    def pre_done(self):
        pass
    
    def no_ack(self):
        pass
    
    def no_on_handler(self):
        pass

    async def on_get_data(self):
        accelerometer = self.accelerometer
        data = ("data\n"
            "%f %f %f"%accelerometer.get_acceleration() + "\n"
            "Free fall: %s"%accelerometer.get_freefall() + "\n"
            "Tapped: %s"%accelerometer.get_tapped() + "\n"
            "Motion detected: %s"%accelerometer.get_motion())
        self.writeline(data)

if __name__ == '__main__':
    try:
        accelerometer = accelerometer.Accelerometer()
    except ValueError as e:
        print(f'exception\n{e}')
        exit()
    accel_parent_proc = AccelerometerParentProcess(accelerometer=accelerometer)
    # Begin session with the parent process. The parent process is collecting the data.
    asyncio.run(accel_parent_proc.begin())
