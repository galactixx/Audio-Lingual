from rich.text import Text
from rich.console import Console

class CLI:
    """Class for managing everything that has to do with output to CLI."""
    def __init__(self, char_limit: int = 100):
        self.char_limit = char_limit
        self.console = Console()

    def cli_print(self, text: str) -> None:
        """Managing printing to CLI using rich syntax."""
        chunks = [text[i:i + self.char_limit] for i in range(0, len(text), self.char_limit)]
        
        for chunk in chunks:
            boxed_text = Text(chunk, style="bold")
            self.console.print(boxed_text)

if __name__ == '__main__':
    cli = CLI()
    cli.cli_print(text='This is a long text that you want to format with word wrapping.')