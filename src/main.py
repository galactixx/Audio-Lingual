from src.cli.cli import CLI
from src.llm.openai import OpenAILLM
from src.models.models import OpenAIInstructions
from src.recognition.recognition import SpeechToText

if __name__ == '__main__':

    # Instantiate OpenAI model and speech recognition
    model = OpenAILLM()
    speech = SpeechToText(device=1, cli_word_max=30)

    # Wait for some audio
    while not speech.audio_deque:
        pass

    # Once there is audio, proces the audio
    speech.process_audio()

    # Process results of converted audio
    speech.convert_audio()

    # Generate messages for OpenAI model
    messages = [OpenAIInstructions.BASIC.value, {"role": "user", "content": speech.generate_text()}]

    # Pass in resulting speech into OpenAI model
    completion = model.get_completion(messages=messages)
    print(completion)