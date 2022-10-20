import asyncio
import concurrent.futures

from i_process import Process
from child_process import ChildProcess
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

class FakeSensorDataViaEchoChildProcess(ChildProcess):
    """
    Fakes sensor data by calling the `echo` shell command.
    """
    def __init__(self):
        super().__init__(
            # String is spread among multiple lines for readability
            'echo "'
                # Escape the backslash character in order to include it
                # in the shell command.
                'ready\\n'
                'data\\n'
                'test_data\\n'
                '\\n'
                'xtra_cmd_1\\n'
                'xtra_cmd_data\\n'
                'done"'
        )

    def on_wait_ready(self):
        self._print("Waiting on ready signal")

    def on_ready(self):
        self._print('ready')

    def on_done(self):
        self._print('done')

    async def on_data(self):
        self._print('data: {}'.format(await self.readline()))

    async def on_xtra_cmd_1(self):
        self._print('xtra_cmd_1: {}'.format(await self.readline()))

class TestChildProcess(ChildProcess):
    """
    Runs test_child.py.

    Exits as soon as the "ready" message_type is received.
    """
    def __init__(self):
        super().__init__('python {}/test_child.py'.format(dir_path))
    
    def on_ready(self):
        self.writeline('exit')
    
    def on_done(self):
        self._print('TestChildProcess is done')

def main():
    child_processes: list[Process] = [
        FakeSensorDataViaEchoChildProcess(),
        FakeSensorDataViaEchoChildProcess(),
        FakeSensorDataViaEchoChildProcess(),
        FakeSensorDataViaEchoChildProcess(),
        TestChildProcess()
    ]
    futures = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # We create a thread for each to-be-executed child process
        # so that asyncio manages one child process per thread.
        for child_process in child_processes:
            futures.append(executor.submit(asyncio.run, child_process.begin()))
    concurrent.futures.wait(futures)

if __name__ == "__main__":
    main()
