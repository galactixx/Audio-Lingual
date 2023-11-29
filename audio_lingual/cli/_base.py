from rich.live import Live
from rich.console import Console

class BaseStreamer(object):
    """
    Base text output in terminal.
    """
    def __init__(self):
        self.live = Live(auto_refresh=False, console=Console(), vertical_overflow="visible")
        self.live.start()

    def end(self):
        self.refresh()
        self.live.stop()

    def refresh(self):
        raise NotImplementedError("Subclasses must implement this method")