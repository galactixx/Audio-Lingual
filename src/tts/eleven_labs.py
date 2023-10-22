from elevenlabs import generate, play
from threading import Thread

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

    def _voice_generation_threaded(self, text: str) -> None:
        """Generates voice message based on inputted text."""
        audio = generate(text=text, voice=self.voice, model=self.model.value)
        
        # Play generated audio
        play(audio)

    def voice_generation(self, text: str) -> Thread:
        """Generate thread of voice generation function."""
        
        # Start a new TTS thread for the generated text
        tts_thread = Thread(target=self._voice_generation_threaded, args=(text,))
        tts_thread.start()

        return tts_thread