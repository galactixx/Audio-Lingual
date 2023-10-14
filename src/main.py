from elevenlabs import generate, play
from src.models.models import OpenAIInstructions
from src.recognition.recognition import SpeechToText
from src.llm.openai import (
    generate_message_prompt,
    OpenAILLM)

if __name__ == '__main__':
    import time

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
    print(speech.generate_text())

    # Generate messages for OpenAI model
    messages = generate_message_prompt(prompt=speech.generate_text(), instruction=OpenAIInstructions.BASIC)
    
    # Pass in resulting speech into OpenAI model
    completion = model.get_completion(messages=messages)
    
    # Generate audio from OpenAI completion using ElevenLabs
    audio = generate(text=completion, voice="Bella", model="eleven_multilingual_v2")
    play(audio)