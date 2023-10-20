from abc import ABC, abstractmethod

from src.models.models import ElevenLabsModels

class BaseTTS(ABC):
    """Base interface for TTS models."""

    @abstractmethod
    def __init__(self, model_name: ElevenLabsModels) -> None:
        pass

    @abstractmethod
    def voice_generation(self, text: str) -> None:
        """Generate final voice generation based on text input."""
        pass