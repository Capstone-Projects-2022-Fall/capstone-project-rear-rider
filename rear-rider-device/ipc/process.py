class Process():
    """
    RearRider process.
    """
    async def begin(self):
        """
        Begin listening to this process.

        NotImplementedError is thrown because the method is meant to be implemented by an inheriting class.
        """
        raise NotImplementedError()

    # async def readline(self):
    #     raise NotImplementedError()
    
    # async def writeline(self, line: str):
    #     raise NotImplementedError()