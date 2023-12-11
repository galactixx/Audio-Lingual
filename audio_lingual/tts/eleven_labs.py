import os

from elevenlabs import generate, play, RateLimitError
from threading import Thread

from audio_lingual.tts._base import BaseTTS
from audio_lingual.models.models import TTSModels
from audio_lingual.voices.voices import ElevenLabsVoices

class ElevenLabs(BaseTTS):
    """
    Interface for Eleven Labs voice generation.
    """
    def __init__(
        self,
        model: TTSModels = TTSModels.ELEVEN_LABS_MULTILINGUAL_V2,
        voice: ElevenLabsVoices = ElevenLabsVoices.BELLA):
        self.model = model
        self.voice = voice
        self.error_api_rate = False

        # The API key is blank or not set
        if not os.environ.get("ELEVEN_API_KEY"):
            raise ValueError("ELEVEN_API_KEY is not set or is blank")

    def _voice_generation_threaded(self, text: str) -> None:
        """
        Generates voice message based on inputted text.
        """

        try:
            audio = generate(text=text, voice=self.voice, model=self.model.value)
        except RateLimitError:
            if not self.error_api_rate:
                print("An error occurred. ElevenLabs API limit reached so no voice will be heard.")
                self.error_api_rate = True
            return
        
        # Play generated audio
        play(audio)

    def voice_generation(self, text: str) -> Thread:
        """
        Generate thread of voice generation function.
        """
        
        tts_thread = Thread(target=self._voice_generation_threaded, args=(text,))
        tts_thread.start()

        return tts_thread