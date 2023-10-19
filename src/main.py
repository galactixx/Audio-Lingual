import time

from collections import deque
import speech_recognition as sr
from elevenlabs import generate, play

from src.llm.openai import OpenAILLM
from src.cli.message import MessageStreamer

class AudioLingual:
    """Speech to text conversion using the speech_recoginition package."""
    def __init__(self,
                 llm_model: OpenAILLM,
                 cli_streamer: MessageStreamer,
                 device: int,
                 cli_word_max: int = 25,
                 pause_threshold: float = 0.8,
                 energy_threshold: int = 300):
        self.llm_model = llm_model
        self.cli_streamer = cli_streamer
        self.device = device
        self.cli_word_max = cli_word_max
        self.pause_threshold = pause_threshold
        self.energy_threshold = energy_threshold

        self.word_counter = 0
        self.audio_deque = deque([])
        self.results_deque = deque([])
        self.mircrophone_main = sr.Microphone(sample_rate=16000, device_index=self.device)

        # Main recognizer to detect live speech
        self.recognizer_main = sr.Recognizer()
        self.recognizer_main.energy_threshold = self.energy_threshold
        self.recognizer_main.pause_threshold = self.pause_threshold
        self.recognizer_main.dynamic_energy_threshold = False

        with self.mircrophone_main as source:
            self.recognizer_main.adjust_for_ambient_noise(source, duration=1)
        print('Microphone is all set-up!')

    @staticmethod
    def microphone_devices() -> list:
        """Return all microphone devices."""
        return sr.Microphone.list_microphone_names()

    def _audio_callback(self, audio: sr.AudioData) -> None:
        """
        Callback function that will be called when speech is detected. Instead of outputting to console
        we will append to audio_deque which will store these values and which will slowly be offloaded.
        """
        self.audio_deque.append(audio)

    def _process_audio(self) -> None:
        """Access audio element in deque and remove and generate translation."""
        audio_data = self.audio_deque.popleft()
        text = self.recognizer_main.recognize_whisper(audio_data=audio_data, language='english')
        self.results_deque.append(text)

    def listen_for_audio(self) -> None:
        """Listen for audio in a loop."""
        while True:
            
            # Listen and detect audio from microphone
            self.listen_with_timeout()

            while self.audio_deque:
                self._process_audio()

                # Pause microphone after processing existing audio
                self.pause_microphone()

                # Generate text from audio recorded
                generated_text = self.generate_text()

                # Output text in in message streamer
                self.cli_streamer.refresh(text=generated_text, do_speaker=False)

                response = self.llm_model.get_completion(prompt=generated_text)

                # Generate audio from completion using ElevenLabs
                audio = generate(text=response, voice="Bella", model="eleven_multilingual_v2")
                play(audio)

                # Output text from chat bot response
                self.cli_streamer.refresh(text=response)

            # Resume listening after generating and playing audio
            self.resume_microphone()

    def listen_with_timeout(self, timeout: int = 5) -> None:
        """Listen for audio with timeout after a certain amount of time."""
        start_time = time.time()
        audio = None

        # Use main microphone to capture any audio
        with self.mircrophone_main as source:
            while time.time() - start_time < timeout:
                audio = self.recognizer_main.listen(source)

                # If audio is captured, exit the loop
                if audio is not None:
                    self._audio_callback(audio=audio)

    def pause_microphone(self) -> None:
        """Pause the microphone to stop listening to ambient noise."""
        self.recognizer_main.energy_threshold = float('inf')

    def resume_microphone(self) -> None:
        """Resume the microphone to listen for speech."""
        self.recognizer_main.energy_threshold = self.energy_threshold

    def generate_text(self) -> str:
        """Generate combined text from converted audio."""
        return self.results_deque.popleft()
    
if __name__ == '__main__':
    audio_lingual = AudioLingual(llm_model=OpenAILLM(),
                                 cli_streamer=MessageStreamer(),
                                 device=1)
    audio_lingual.listen_for_audio()