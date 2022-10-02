import asyncio
import threading
from process import Process

class ChildProcess(Process):
    """
    A child process executed in a shell program.
    """
    def __init__(self, program: str):
        self._program = program
        self._stdin = None
        self._stdout = None
    
    async def readline(self):
        """
        Read a line from the child process's stdout.
        Raises EOFError when EOF has been reached.
        """
        line = await self._stdout.readline()
        if len(line) == 0:
            raise EOFError()
        return line.decode().rstrip()
    
    def writeline(self, message: str):
        """
        Write something into the child process's stdin.
        """
        self._stdin.write(bytes('{}\n'.format(message), 'utf8'))

    def _print(self, message: str):
        print('{}: {}'.format(threading.current_thread().native_id, message), flush=True)

    async def begin(self):
        """
        Starts the execution of the child process.
        This call resolves when the child process stops execution.
        """
        proc = await asyncio.subprocess.create_subprocess_shell(
            self._program,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE)
        self._stdin = proc.stdin
        self._stdout = proc.stdout

        # We should await the child process's `ready` signal before attempting to signal for child process specific data. This is done to ensure the signal handler is ready.
        self.on_wait_ready()

        EXPECTED_READY_SIGNAL = 'ready'
        ready_signal = await self.readline()

        if ready_signal != EXPECTED_READY_SIGNAL:
            self._print(ready_signal)
            # `ready` was the expected first line read, but it was not received.
            raise Exception("Expected the child process\'s ready signal to be `{expected_ready_signal}`"
                    .format(expected_ready_signal=EXPECTED_READY_SIGNAL))

        self.on_ready()

        while True:
            try:
                message_type = await self.readline()
            except EOFError:
                raise Exception("EOF not expected")
            if len(message_type) == 0:
                # Skip empty message_types
                continue
            elif message_type == EXPECTED_READY_SIGNAL:
                raise Exception("ready not expected")
            elif message_type == 'done':
                break
            else:
                await self._on_message(message_type)
        
        proc_return_code = await proc.wait()
        if proc_return_code != 0:
            raise Exception("Expected the child process to exit successfully.\n"
                    "\tThe child process exited with an error code of {}\n"
                    .format(proc_return_code))

        self.on_done()
    
    def on_wait_ready(self):
        """
        Unimplemented.
        """
        pass
    
    def on_done(self):
        """
        Unimplemented.
        """
        pass

    def on_ready(self):
        """
        Unimplemented.
        """
        pass

    async def _on_message(self, message_type: str):
        """
        Calls the message_type handler of the class.
        The handler of message_type should be defined as:

        1. Coroutine function.
        2. Its name as on_message_type.

        For example:
        Imagine message_type == "data", then the handler for this message_type
        should be named "on_data".
        
        ```python
        class ChildProcessImplementation(ChildProcess):
            # ...
            async def on_data():
                \"""
                Implementation
                \"""
            # ...
        ```
        """
        await self.__getattribute__('on_{}'.format(message_type))()
