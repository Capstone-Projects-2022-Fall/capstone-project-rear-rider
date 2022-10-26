import asyncio
import concurrent.futures
from ipc.i_process import Process
from accelerometer_child_proc import AccelerometerChildProcess
from bluetooth_server_child_proc import BluetoothServerChildProcess
from camera_child_proc import CameraChildProcess

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

def main():
    bt_server_process = BluetoothServerChildProcess()
    camera_proc = CameraChildProcess()
    #accelerometer_proc = AccelerometerChildProcess(buf_size=32, fps=1,
    #    bt_server_proc=bt_server_process)
    child_processes: list[Process] = [
        #accelerometer_proc,
        bt_server_process,
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
