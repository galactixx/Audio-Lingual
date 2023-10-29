from TTS.api import TTS
import pyaudio

from src.tts.base import BaseTTS
from src.models.models import TTSModels

class Coqui(BaseTTS):
    """Interface for Coqui voice generation."""
    def __init__(self,
                 model: TTSModels = TTSModels.COQUI_GLOW_TTS):
        pass