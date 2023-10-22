import time

from rich.panel import Panel
from rich.box import MINIMAL
from rich.text import Text

from src.cli.base import BaseStreamer

class MessageStreamer(BaseStreamer):
    """"""
    def __init__(self, speaker_name: str = 'Audio Lingual', streaming_delay: float = 0.02):
        super().__init__()
        self.speaker_name = speaker_name
        self.streaming_delay = streaming_delay

        # Message history
        self.message = Text()

    def refresh(self, text: str, do_speaker: bool = True, do_greeting: bool = False):
        """"""
        if do_greeting:
            self.message.append(f'{self.speaker_name}: ', style="bold")
        elif do_speaker:
            self.message.append(f'\n{self.speaker_name}: ', style="bold")
        else:
            self.message.append(f'\nPerson: ', style="bold")

        # Output text in streaming style, character by character
        text_strip = text.strip()
        for char in text_strip:

            # Add new character to the message
            self.message.append(char, style="bold")
            panel = Panel(self.message, box=MINIMAL)
            self.live.update(panel)
            self.live.refresh()

            # Adjust the delay as needed
            time.sleep(0.05)