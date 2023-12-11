import json
from threading import Thread

import torch
import sounddevice as sd
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer

from audio_lingual.tts._base import BaseTTS
from audio_lingual.models.models import CoquiModelGroup, TTSModels
from audio_lingual.models.language_codes import LanguageCodes
from audio_lingual.utils import collect_coqui_models_json_file

with open('config.json') as config_file:
    config = json.load(config_file)

MODEL_DIRECTORY = config['downloaded_models_path']

class Coqui(BaseTTS):
    """
    Interface for Coqui voice generation.
    """
    def __init__(
        self,
        model: TTSModels = TTSModels.COQUI_GLOW_TTS,
        language: LanguageCodes = LanguageCodes.ENGLISH,
        model_group: CoquiModelGroup = CoquiModelGroup.LJSPEECH):
        self.model = model
        self.language = language
        self.model_group = model_group

        # Based on specified model, download model if it needs to be downloaded
        self.model_manager = ModelManager(
            collect_coqui_models_json_file(),
            output_prefix=MODEL_DIRECTORY,
            progress_bar=True
        )

        model_path, config_path, model_item = self._download_model()
        vocoder_model_path, vocoder_config_path, _ = self.model_manager.download_model(model_item["default_vocoder"])
        
        self.synthesizer = self._initialize_synthesizer(model_path, config_path, vocoder_model_path, vocoder_config_path)

    def _generate_directory_name(self) -> str:
        """
        Generate model directory based on parameters.
        """
        
        return f'tts_models/{self.language.value}/{self.model_group.value}/{self.model.value}'

    def _download_model(self):
        """
        Download model using ModelManager.
        """

        return self.model_manager.download_model(
            self._generate_directory_name()
        )

    def _initialize_synthesizer(
        self, tts_checkpoint: str,
        tts_config_path: str,
        vocoder_checkpoint: str,
        vocoder_config_path: str
    ):
        """
        Initialize the synthesizer for later use.
        """

        use_cuda = torch.cuda.is_available()
        return Synthesizer(
            tts_checkpoint=tts_checkpoint,
            tts_config_path=tts_config_path,
            vocoder_checkpoint=vocoder_checkpoint,
            vocoder_config=vocoder_config_path,
            use_cuda=use_cuda
        )

    def _voice_generation_threaded(self, text: str) -> None:
        """
        Generate final voice generation based on text input.
        """

        speech = self.synthesizer.tts(text)

        # Play the resulting speech using sounddevice
        sd.play(speech, samplerate=23050)

    def voice_generation(self, text: str) -> Thread:
        """
        Generate thread of voice generation function.
        """

        tts_thread = Thread(
            target=self._voice_generation_threaded,
            args=(text,)
        )
        tts_thread.start()

        return tts_thread