from TTS.api import TTS
import pyaudio

from src.tts.base import BaseTTS
from src.models.models import CoquiModels

class Coqui(BaseTTS):
    """Interface for Coqui voice generation."""
    def __init__(self,
                 model: CoquiModels = CoquiModels.GLOW_TTS):
        pass