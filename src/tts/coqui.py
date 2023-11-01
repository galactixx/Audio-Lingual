import pyaudio
import json
import torch
from threading import Thread
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

        # Coqui models json path
        model_json_path = collect_coqui_models_json_file()

        # Based on specified model, download model if it needs to be downloaded
        manager = ModelManager(model_json_path, output_prefix=MODEL_DIRECTORY, progress_bar=True)

        # Use the ModelManager to download a model
        model_path, config_path, model_item = manager.download_model(
            f'tts_models/{self.language.value}/{self.model_group.value}/{self.model.value}')
        
        # Download the default vocoder for the TTS model
        vocoder_model_path, vocoder_config_path, _ = manager.download_model(model_item["default_vocoder"])

        # Initialize the synthesizer
        use_cuda = torch.cuda.is_available()
        self.synthesizer = Synthesizer(
            tts_checkpoint=model_path,
            tts_config_path=config_path,
            vocoder_checkpoint=vocoder_model_path,
            vocoder_config=vocoder_config_path,
            use_cuda=use_cuda
        )

        # Initialize PyAudio and open a stream
        p = pyaudio.PyAudio()
        self.stream = p.open(format=pyaudio.paInt16,
                             channels=1,
                             rate=16000,
                             input=True,
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
    

Coqui()