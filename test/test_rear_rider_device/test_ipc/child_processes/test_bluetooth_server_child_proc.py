"""
Refactored from `rear_rider_device/bluetooth_server_child_proces.py`.
"""
import asyncio
import concurrent.futures
import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    # This file should be in `test/rear_rider_device/test_ipc/child_processes` so we need to travel
    # up 3 directories.
    f'{os.pardir}/../../..')
)
sys.path.append(PROJECT_ROOT)
from rear_rider_device.bluetooth_server_child_proc import BluetoothServerChildProcess
from rear_rider_device.leds_child_proc import LedsChildProcess

if __name__ == '__main__':
    leds_proc = LedsChildProcess()
    proc = BluetoothServerChildProcess(leds_child_process=leds_proc)
    # parent = TestParent(leds_proc)
    processes: list = [
        proc,
        leds_proc
    ]
    futures = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # We create a thread for each to-be-executed child process
        # so that asyncio manages one child process per thread.
        for process in processes:
            futures.append(executor.submit(asyncio.run, process.begin()))
    print(len(futures))
    concurrent.futures.wait(futures)
