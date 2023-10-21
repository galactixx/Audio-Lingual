from elevenlabs import generate, play

from src.tts.base import BaseTTS
from src.models.models import ElevenLabsModels
from src.voices.voices import ElevenLabsVoices

class ElevenLabs(BaseTTS):
    """Base interface for Eleven Labs voice generation."""
    def __init__(self,
                 model: ElevenLabsModels = ElevenLabsModels.MULTILINGUAL_V2,
                 voice: ElevenLabsVoices = ElevenLabsVoices.BELLA):
        self.model = model
        self.voice = voice

    def voice_generation(self, text: str) -> None:
        """Generates voice message based on inputted text."""
        audio = generate(text=text, voice=self.voice, model=self.model.value)
        
        # Play generated audio
        play(audio)