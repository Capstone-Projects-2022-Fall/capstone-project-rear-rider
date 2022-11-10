import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__),
                  f'{os.pardir}')
)
sys.path.append(PROJECT_ROOT)

import asyncio
import concurrent.futures
from rear_rider_device.ipc.i_process import Process
from rear_rider_device.accelerometer_child_proc import AccelerometerChildProcess
from rear_rider_device.bluetooth_server_child_proc import BluetoothServerChildProcess
from rear_rider_device.camera_child_proc import CameraChildProcess
from rear_rider_device.lidar_child_proc import LidarChildProcess

from rear_rider_device.leds_child_proc import LedsChildProcess 
dir_path = os.path.dirname(os.path.realpath(__file__))

def main():
    leds_child_proc = LedsChildProcess()
    bt_server_process = BluetoothServerChildProcess(
            leds_child_process=leds_child_proc)
    accelerometer_proc = AccelerometerChildProcess(buf_size=32, fps=1,
        bt_server_proc=bt_server_process)
    lidar_child_proc = LidarChildProcess(led_child_proc=leds_child_proc)
    # camera_proc = CameraChildProcess(bt_server_proc=bt_server_process)
    child_processes: list[Process] = [
        leds_child_proc,
        accelerometer_proc,
        bt_server_process,
        lidar_child_proc
        # camera_proc
    ]
    futures = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # We create a thread for each to-be-executed child process
        # so that asyncio manages one child process per thread.
        for child_process in child_processes:
            futures.append(executor.submit(asyncio.run, child_process.begin()))
    print(len(futures))
    concurrent.futures.wait(futures)

if __name__ == "__main__":
    main()
