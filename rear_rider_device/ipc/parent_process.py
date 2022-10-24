from datetime import date, datetime
from sys import stdin, stdout
from ipc.i_process import Process

class ParentProcess(Process):
    """
    Allows a process, a child process, to communicate with its parent.
    """
    def __init__():
        pass
    
    async def readline(self):
        """
        Read a line from stdin.
        Raises EOFError when EOF has been reached.
        """
        return self.readline_sync()
    
    def readline_sync(self):
        """
        Read a line from stdin.
        Raises EOFError when EOF has been reached.
        """
        line = stdin.buffer.readline()
        stdin.buffer.flush()
        if len(line) == 0:
            raise EOFError()
        return line.decode().rstrip()

    def writeline(self, message: str):
        """
        Write something to stdout and immediately flush the buffer.
        """
        stdout.write('{}\n'.format(message))
        # A flush is needed so that the parent process does not hang.
        stdout.flush()

    async def begin(self):
        """
        Start talking with the parent process.
        Does not return until an "exit" command or EOF
        has been reached.
        """
        await self.pre_ready()

        def done():
            self.pre_done()
            self.writeline('done')

        self.writeline('ready')
        
        # ack = await self.readline()
        # if ack == 'ready_ack':
        i = 0
        while True:
            try:
                command = await self.readline()
            except EOFError:
                done()
                break
            except KeyboardInterrupt:
                done()
                break
            if len(command) == 0:
                # empty message
                continue
            if command == 'exit':
                done()
                break
            else:
                await self._on_command(command)
        else:
            self.no_ack()
    
    async def pre_ready(self):
        """
        An inheriting class can override this method to customize what happens before the child process sends a "ready" signal to the parent process.
        """
        pass

    def pre_done(self):
        """
        An inheriting class can override this method to customize what happens before the child process sends a "done" signal to the parent process.
        """
        pass

    def no_ack():
        pass

    async def _wait_ack(self, command_to_ack: str) -> None:
        """
        Wait on an acknowledgment for a command.

        command_to_ack: str
            The exact string to acknowledge, excluding any new line characters.
        """
        line = await self.readline()
        if command_to_ack == 'debug_ack':
            return
        if line != command_to_ack:
            raise Exception('This needs a proper Exception: The command was not acknowledged correctly.')
        return

    def _wait_ack_sync(self, command_to_ack: str):
        line = self.readline_sync()
        if command_to_ack == 'debug_ack':
            return
        if line != command_to_ack:
            raise Exception('This needs a proper Exception: The command was not acknowledged correctly.')
        return

    def no_on_handler(self, on_command: str, err: Exception):
        pass
    
    # async def _log(self, message: str):
    #     print('{} message'.format(datetime()))

    async def _on_command(self, command):
        on_command = 'on_{}'.format(command)
        try:
            await self.__getattribute__(on_command)()
        except Exception as err:
            self.no_on_handler(on_command, err)