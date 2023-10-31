from abc import ABC, abstractmethod
from threading import Thread

class BaseTTS(ABC):
    """Base interface for TTS models."""

    @abstractmethod
    def _voice_generation_threaded(self, text: str) -> None:
        """Generate final voice generation based on text input."""
        pass

    @abstractmethod
    def voice_generation(self, text: str) -> Thread:
        """Generate thread of voice generation function."""
        pass