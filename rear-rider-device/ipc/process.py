class Process():
    """
    RearRider process.
    """
    async def begin(self):
        """
        Begin listening to this process.
        """
        raise NotImplementedError()

    # async def readline(self):
    #     raise NotImplementedError()
    
    # async def writeline(self, line: str):
    #     raise NotImplementedError()