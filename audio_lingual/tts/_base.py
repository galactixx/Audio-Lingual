from abc import ABC, abstractmethod
from threading import Thread

class BaseTTS(ABC):
    """Base interface for TTS models."""
    @abstractmethod
    def _voice_generation_threaded(self, text: str) -> None:
        pass

    @abstractmethod
    def voice_generation(self, text: str) -> Thread:
        pass