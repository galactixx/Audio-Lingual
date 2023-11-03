import json
from threading import Thread

import numpy as np
import pyaudio
import torch
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer

from src.tts.base import BaseTTS
from src.models.models import CoquiModelGroup, TTSModels
from src.models.language_codes import LanguageCodes
from src.utils import collect_coqui_models_json_file

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
        self.model_manager = ModelManager(collect_coqui_models_json_file(), output_prefix=MODEL_DIRECTORY, progress_bar=True)

        # Use the ModelManager to download a model
        model_path, config_path, model_item = self._download_model()
        vocoder_model_path, vocoder_config_path, _ = self.model_manager.download_model(model_item["default_vocoder"])
        
        self.synthesizer = self._initialize_synthesizer(model_path, config_path, vocoder_model_path, vocoder_config_path)
        self.stream = self._initialize_audio_stream()

    def _download_model(self):
        return self.model_manager.download_model(f'tts_models/{self.language.value}/{self.model_group.value}/{self.model.value}')

    def _initialize_synthesizer(self, tts_checkpoint, tts_config_path, vocoder_checkpoint, vocoder_config_path):
        use_cuda = torch.cuda.is_available()
        return Synthesizer(tts_checkpoint=tts_checkpoint,
                           tts_config_path=tts_config_path,
                           vocoder_checkpoint=vocoder_checkpoint,
                           vocoder_config=vocoder_config_path,
                           use_cuda=use_cuda)

    def _initialize_audio_stream(self):
        p = pyaudio.PyAudio()
        return p.open(format=pyaudio.paInt16,
                      channels=1,
                      rate=16000,
                      output=True,
                      frames_per_buffer=1024)

    def _voice_generation_threaded(self, text: str) -> None:
        """Generate final voice generation based on text input."""
        speech = self.synthesizer.tts(text)
        self.stream.write(speech)

    def voice_generation(self, text: str) -> Thread:
        """Generate thread of voice generation function."""
        tts_thread = Thread(target=self._voice_generation_threaded, args=(text,))
        tts_thread.start()

        return tts_thread