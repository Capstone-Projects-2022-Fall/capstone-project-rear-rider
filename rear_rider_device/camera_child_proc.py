import asyncio
from datetime import datetime
from ipc.child_process import ChildProcess
from typing import Deque

from bluetooth_server_child_proc import BluetoothServerChildProcess

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

class CameraChildProcess(ChildProcess):
    def __init__(self, bt_server_proc: BluetoothServerChildProcess):
        self.ready = asyncio.Future()
        #self.bt_server_proc = bt_server_proc

    async def on_ready(self):
        """
        An empty function.

        An inheriting class can override this method to customize what happens when the child process is ready for communication
        """
        self.start_time = datetime.now()
        self._print('CameraChildProcess is ready.')
        # try:
            # await self.writeline('ready_ack')
        try:
            await self.writeline('get_stream')
        except:
            pass
        self.ready.set_result(None)
        self._print('after_on_ready')
    

    async def on_wait_ready(self):
        """
        An empty function.

        An inheriting class can override this method to customize what happens before the parent process receives a ready signal from the child process.
        """
        pass
    
    def on_done(self):
        """
        An empty function.

        An inheriting class can override this method to customize what happens when the child process is done communicating with the parent process. 
        """
        pass