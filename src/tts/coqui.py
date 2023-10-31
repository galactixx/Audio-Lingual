from TTS.api import TTS
import pyaudio
import json
from threading import Thread

from src.tts.base import BaseTTS
from TTS.utils.manage import ModelManager
from src.models.models import CoquiModelGroup, TTSModels
from src.models.language_codes import LanguageCodes

with open('config.json') as config_file:
    config = json.load(config_file)

MODEL_DIRECTORY = config['downloaded_models_path']

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
        manager = ModelManager()

        # Use the ModelManager to download a model
        model_path, config_path, model_item = manager.download_model(
            f'tts_models/{self.language}/{self.model_group}/{self.model}',
            out_path=MODEL_DIRECTORY,
            progress_bar=True)

    def _voice_generation_threaded(self, text: str) -> None:
        """Generate final voice generation based on text input."""
        pass

    def voice_generation(self, text: str) -> Thread:
        """Generate thread of voice generation function."""
        pass