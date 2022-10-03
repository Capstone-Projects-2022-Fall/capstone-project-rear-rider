from sys import stdin, stdout
from process import Process

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
        line = stdin.buffer.readline()
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
        self.pre_ready()
        self.writeline('ready')

        i = 0
        while True:
            try:
                command = await self.readline()
            except EOFError:
                break
            if len(command) == 0:
                # empty message
                continue
            if command == 'exit':
                break
            else:
                await self._on_command(command)
        
        self.pre_done()
        self.writeline('done')
    
    def pre_ready(self):
        """
        An inheriting class can override this method to customize what happens before the child process sends a "ready" signal to the parent process.
        """
        pass

    def pre_done(self):
        """
        An inheriting class can override this method to customize what happens before the child process sends a "done" signal to the parent process.
        """
        pass

    async def _on_command(self, command):
        await self.__getattribute__('on_{}'.format(command))()