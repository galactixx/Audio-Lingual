from typing import Optional

import numpy as np
from speech_recognition import WaitTimeoutError
from collections import deque
import speech_recognition as sr

class Microphone:
    """Detect and process audio from microphone"""
    def __init__(self,
                 device: int,
                 sample_rate: int = 16000,
                 energy_threshold: int = 300,
                 silence_threshold: int = 500,
                 pause_threshold: float = 0.8):
        self.device = device
        self.sample_rate = sample_rate
        self.pause_threshold = pause_threshold
        self.energy_threshold = energy_threshold
        self.silence_threshold = silence_threshold

        # Initial queues to tracker audio and text results
        self.audio_deque = deque([])
        self.results_deque = deque([])

        # Set-up initial microphone
        self.mircrophone_main = sr.Microphone(sample_rate=self.sample_rate, device_index=self.device)

    @staticmethod
    def microphone_devices() -> list:
        """Return all microphone devices."""
        return sr.Microphone.list_microphone_names()
    
    def pause_microphone(self) -> None:
        """Pause the microphone to stop listening to ambient noise."""
        self.recognizer_main.energy_threshold = float('inf')

    def resume_microphone(self) -> None:
        """Resume the microphone to listen for speech."""
        self.recognizer_main.energy_threshold = self.energy_threshold

    def _is_silent(self, audio_data: sr.AudioData) -> bool:
        """Determine if audio data recieved is not valid (i.e. silence)"""
        audio_levels = np.frombuffer(audio_data, dtype=np.int16)
        return np.max(audio_levels) < self.silence_threshold

    def _audio_callback(self, audio: sr.AudioData) -> None:
        """Callback function that will be called when speech is detected."""
        self.audio_deque.append(audio)
    
    def set_up_recognizer(self) -> None:
        """Set-up main recognizer to detect live speech"""
        self.recognizer_main = sr.Recognizer()
        self.recognizer_main.energy_threshold = self.energy_threshold
        self.recognizer_main.pause_threshold = self.pause_threshold
        self.recognizer_main.dynamic_energy_threshold = False

    def process_audio(self) -> None:
        """Access audio element in deque and remove and generate translation."""
        while self.audio_deque:
            audio_data = self.audio_deque.popleft()
            text = self.recognizer_main.recognize_whisper(audio_data=audio_data, language='english')
            self.results_deque.append(text)

    def generate_text(self) -> str:
        """Generate combined text from converted audio."""
        text = []
        while self.results_deque:
            result = self.results_deque.popleft()
            text.append(result)
        return ' '.join(text)
    
    def listen_with_timeout(self, timeout: int = 5, phrase_time_limit: Optional[int] = None) -> None:
        """Listen for audio with timeout after a certain amount of time."""
        audio = None

        # Use main microphone to capture any audio
        while True:
            try:
                with self.mircrophone_main as source:
                    self.recognizer_main.adjust_for_ambient_noise(source, duration=1)
                    audio = self.recognizer_main.listen(source,
                                                        timeout=timeout,
                                                        phrase_time_limit=phrase_time_limit)

                # If audio is captured and not actually silence, callback and then exit the loop
                if audio is not None:
                    if not self._is_silent(audio_data=audio.frame_data):
                        self._audio_callback(audio=audio)
                        break
            except WaitTimeoutError:
                pass