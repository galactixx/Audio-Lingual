from TTS.api import TTS
import pyaudio

from src.utils import coqui_gather_and_download_model_by_selection
from src.tts.base import BaseTTS
from src.models.models import CoquiModelGroup, TTSModels
from src.models.language_codes import LanguageCodes

class Coqui(BaseTTS):
    """Interface for Coqui voice generation."""
    def __init__(self,
                 model: TTSModels = TTSModels.COQUI_GLOW_TTS,
                 language: LanguageCodes = LanguageCodes.ENGLISH,
                 model_group: CoquiModelGroup = CoquiModelGroup.LJSPEECH):
        self.model = model
        self.language = language
        self.model_group = model_group

        # Based on specified model, download model if it needs to be downloaded
        coqui_gather_and_download_model_by_selection(model=self.model,
                                                     language=self.model,
                                                     model_gorup=self.model_group)