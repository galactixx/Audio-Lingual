from elevenlabs import generate, play

from src.models.models import ElevenLabsModels
from src.voices.voices import ElevenLabsVoices

class ElevenLabs:
    """Base interface for Eleven Labs voice generation."""
    def __init__(self,
                 model: ElevenLabsModels = ElevenLabsModels.MULTILINGUAL_V2,
                 voice: ElevenLabsVoices = ElevenLabsVoices.GRACE):
        self.model = model
        self.voice = voice

    def voice_generation(self, text: str) -> None:
        """"""
        
        # Output introduction to chat bot
        audio = generate(text=text, voice=self.voice, model=self.model)
        play(audio)