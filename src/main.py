from src.tts.eleven_labs import ElevenLabs
from src.llm.openai import OpenAILLM
from src.cli.message import MessageStreamer
from src.mic.mic import Microphone
from src.voices.voices import Greetings

class AudioLingual:
    """
    Main application that detects audio from microphone, converts to text,
    intputs text to an LLM, takes LLM response which is then returned as a TTS response.
    """
    def __init__(self,
                 greeting: Greetings,
                 llm_model: OpenAILLM,
                 tts_model: ElevenLabs,
                 microphone: Microphone,
                 cli_streamer: MessageStreamer):
        self.llm_model = llm_model
        self.tts_model = tts_model
        self.microphone = microphone
        self.cli_streamer = cli_streamer

        # Generate greeting and end 
        tts_thread = self.tts_model.voice_generation(text=greeting)
        self.cli_streamer.refresh(text=greeting, do_greeting=True)
        tts_thread.join()

    def listen_for_audio(self) -> None:
        """Listen for audio in a loop."""
            
        # Listen and detect audio from microphone
        self.microphone.listen_with_timeout()

        # Process any audio after listening
        self.microphone.process_audio()

        # Pause microphone after processing existing audio
        self.microphone.pause_microphone()

        # Generate text from audio recorded
        generated_text = self.microphone.generate_text()

        # Output text in in message streamer
        self.cli_streamer.refresh(text=generated_text, do_speaker=False)

        # Get response from LLM
        response = self.llm_model.get_completion(prompt=generated_text)

        # Start a new TTS thread for the generated text
        tts_thread = self.tts_model.voice_generation(text=response)

        # Output text from chat bot response
        self.cli_streamer.refresh(text=response)
        tts_thread.join()

        # Resume listening after generating and playing audio
        self.microphone.resume_microphone()
    
if __name__ == '__main__':
    audio_lingual = AudioLingual(greeting=Greetings.BASIC,
                                 llm_model=OpenAILLM(),
                                 tts_model=ElevenLabs(),
                                 microphone=Microphone(device=1),
                                 cli_streamer=MessageStreamer())
    
    # Inititalize recognizer
    audio_lingual.microphone.set_up_recognizer()
    
    # Listen for audio
    while True:
        audio_lingual.listen_for_audio()