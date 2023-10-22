from abc import ABC, abstractmethod
from threading import Thread

from src.models.models import ElevenLabsModels

class BaseTTS(ABC):
    """Base interface for TTS models."""

    @abstractmethod
    def __init__(self, model_name: ElevenLabsModels) -> None:
        pass

    @abstractmethod
    def _voice_generation_threaded(self, text: str) -> None:
        """Generate final voice generation based on text input."""
        pass

    @abstractmethod
    def voice_generation(self, text: str) -> Thread:
        """Generate thread of voice generation function."""
        pass