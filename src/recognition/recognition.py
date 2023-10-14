from collections import deque
import speech_recognition as sr

class SpeechToText:
    """Speech to text conversion using the speech_recoginition package."""
    def __init__(self, device: int, cli_word_max: int = 25):
        self.device = device
        self.cli_word_max = cli_word_max

        self.word_counter = 0
        self.results = []
        self.audio_deque = deque([])
        self.mircrophone_main = sr.Microphone(sample_rate=16000, device_index=self.device)

        # Main recognizer to detect live speech
        self.recognizer_main = sr.Recognizer()
        self.recognizer_main.energy_threshold = 300
        self.recognizer_main.pause_threshold = 0.8
        self.recognizer_main.dynamic_energy_threshold = False

        with self.mircrophone_main as source:
            self.recognizer_main.adjust_for_ambient_noise(source, duration=1)
        self.recognizer_main.listen_in_background(self.mircrophone_main, self._audio_callback, phrase_time_limit=3)
        print('Mircrophone is all set-up!')

    @staticmethod
    def microphone_devices() -> list:
        """Return all microphone devices."""
        return sr.Microphone.list_microphone_names()

    def _audio_callback(self, _, audio: sr.AudioData) -> None:
        """Callback function that will be called when speech is detected. Instead of outputting to console
        we will append to audio_deque which will store these values and which will slowly be offloaded."""
        self.audio_deque.append(audio)

    def process_audio(self) -> str:
        """Access audio element in deque and remove and generate translation."""
        audio_data = self.audio_deque.popleft()
        text = self.recognizer_main.recognize_whisper(audio_data=audio_data, language='english')
        return text
    
    def convert_audio(self) -> None:
        """Continually check audio_deque to see if there are any audio files to be converted to text."""
        while self.audio_deque:
            text_from_audio = self.psrocess_audio()
            self.results.append(text_from_audio)

    def generate_text(self) -> str:
        """Generate combined text from converted audio."""
        return ' '.join(self.results)