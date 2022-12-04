import threading
from typing import Callable

class ThreadedRepeat(threading.Timer):
    '''
    Repeat a function at a set interval.
    '''
    def __init__(self, interval_seconds: float, function: Callable[[], None]):
        super().__init__(interval_seconds, function)

    def run(self):
        while not self.finished.wait(self.interval):
            self.function()

    def update_interval(self, interval_seconds: float):
        '''
        The interval in seconds.
        '''
        self.interval = interval_seconds
