import asyncio
import threading
from typing import Union
from ipc.i_process import Process

class ChildProcess(Process):
    """
    A child process to be executed in a shell program.


    ## Test
    
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
    _program: str
    "The command to execute as the program."
    _stdin: Union[asyncio.StreamWriter, None]
    "A pipe to the child's input."
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
    
    async def writeline(self, message: str):
        """
        Write something into the child process's stdin.
        """
        self._stdin.write(bytes('{}\n'.format(message), 'utf8'))
        await self._stdin.drain()

    def _print(self, message: str):
        for message_line in message.splitlines():
            print('{} {}: {}'.format(threading.current_thread().native_id, self._get_name(), message_line))
        print(flush=True)

    async def begin(self):
        """
        Starts the execution of the child process.
        This call resolves when the child process stops execution.
        """
        async def _begin():
            proc = await asyncio.subprocess.create_subprocess_shell(
                self._program,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE)
            self._stdin = proc.stdin
            self._stdout = proc.stdout

            # We should await the child process's `ready` signal before attempting to signal for child process specific data. This is done to ensure the signal handler is ready.
            await self.on_wait_ready()

            EXPECTED_READY_SIGNAL = 'ready'
            ready_signal = await self.readline()

            if ready_signal != EXPECTED_READY_SIGNAL:
                self._print(ready_signal)
                # `ready` was the expected first line read, but it was not received.
                raise Exception("Expected the child process\'s ready signal to be `{expected_ready_signal}` not `{ready_signal}`"
                        .format(expected_ready_signal=EXPECTED_READY_SIGNAL, ready_signal=ready_signal))

            await self.on_ready()

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
        
        try:
            await _begin()
        except Exception as err:
            self._print('Exception on childprocess.\n{}'.format(err))
    
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

    async def on_ready(self):
        """
        An empty function.

        An inheriting class can override this method to customize what happens when the child process is ready for communication
        """
        pass
    
    async def _wait_ack(self, command_to_ack: str) -> None:
        """
        Wait on an acknowledgment for a command.

        command_to_ack: str
            The exact string to acknowledge, excluding any new line characters.
        """
        line = await self.readline()
        if line != command_to_ack:
            raise Exception('This needs a proper Exception: The command was not acknowledged correctly.')
        return

    def no_on_handler(self, on_command, err):
        raise NotImplementedError('no_on_handler is not implemented')

    async def _on_message(self, message_type: str):
        """
        Calls the message_type handler of the class.
        """
        on_message_type = 'on_{}'.format(message_type)
        try:
            await self.__getattribute__(on_message_type)()
        except AttributeError as err:
            self.no_on_handler(on_message_type, err)

    def _get_name(self) -> str:
        return 'ChildProcess'
