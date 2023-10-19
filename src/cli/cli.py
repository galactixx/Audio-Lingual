import time

from rich.panel import Panel
from rich.box import MINIMAL
from rich.text import Text

from src.cli.base import BaseCLI

class MessageCLI(BaseCLI):
    """"""
    def __init__(self, speaker_name: str, streaming_delay: float = 0.02):
        super().__init__()
        self.speaker_name = speaker_name
        self.streaming_delay = streaming_delay

        self.message = Text()

    def refresh(self, text: str, do_speaker: bool = True):
        """"""
        if do_speaker:
            self.message.append(f'{self.speaker_name}: ', style="bold")
        
        else:
            self.message.append(f'\nNick: ', style="bold")

        # Output text in streaming style, character by character
        for char in text:

            # Add new character to the message
            self.message.append(char, style="bold")
            panel = Panel(self.message, box=MINIMAL)
            self.live.update(panel)
            self.live.refresh()

            # Adjust the delay as needed
            time.sleep(0.05)