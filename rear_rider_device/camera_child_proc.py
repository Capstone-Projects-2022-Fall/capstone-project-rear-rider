import asyncio
import os 
from datetime import datetime
from ipc.child_process import ChildProcess

dir_path = os.path.dirname(os.path.realpath(__file__))

class CameraChildProcess(ChildProcess):
    def __init__(self):
        super().__init__(f'python {dir_path}/camera_proc.py')
        self.ready = asyncio.Future()
        #self.bt_server_proc = bt_server_proc

    def _get_name(self) -> str:
        return 'CameraChildProcess'

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
        except Exception as e:
            self._print(f'Error in on_ready:{e.message}')
        self.ready.set_result(None)
        self._print('after_on_ready') 

    async def on_wait_ready(self):
        """
        An empty function.

        An inheriting class can override this method to customize what happens before the parent process receives a ready signal from the child process.
        """
   
    def on_done(self):
        """
        An empty function.

        An inheriting class can override this method to customize what happens when the child process is done communicating with the parent process. 
        """
