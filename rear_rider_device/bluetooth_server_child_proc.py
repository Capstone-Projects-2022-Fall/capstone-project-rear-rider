from ipc.child_process import ChildProcess

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

class BluetoothServerChildProcess(ChildProcess):
    def __init__(self):
        super().__init__("python {}/bluetooth.py".format(dir_path))

    def _print_header(self, message: str):
        return super()._print('==== Bluetooth Process ====\n{}'.format(message))

    async def on_ready(self):
        self._print('==== Bluetooth Process: on_ready ====')
        await self.writeline('sensor_data_stream')

    def on_done(self):
        self._print('==== Bluetooth : on_done')
    
    async def on_sensor_data_stream_ready(self):
        self._print_header('sensor_data_stream begin')
        
        self._print_header('sensor_data_stream_end')
    
    async def on_set_data_ack(self):
        self._print('on_set_data_ack')

    async def on_read_accelerometer(self):
        self._print('on_read_accelerometer')
