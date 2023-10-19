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

    def refresh(self, text: str, do_speaker: bool = True):
        """"""
        text_display = Text()
        panel = Panel(text_display, box=MINIMAL)
        self.live.update(panel)

        if do_speaker:
            text_display.append(f'{self.speaker_name}: ', style="bold")

        for char in text:
            text_display.append(char, style="bold")
            self.live.refresh()

            # Adjust the delay as needed
            time.sleep(self.streaming_delay)

if __name__ == '__main__':
    message_box = MessageCLI(speaker_name='Grace')
    message_box.refresh(text='This is a streaming text example.')