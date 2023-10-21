import threading
from gtts import gTTS
import os
from src.cli.message import MessageStreamer

# Function for handling CLI input and output
def cli_task():
    cli_streamer = MessageStreamer()
    while True:
        user_input = input("Enter text (or 'exit' to quit): ")

        if user_input == 'exit':
            break

        # Output text to CLI
        cli_streamer.refresh(text=user_input)

        # Start a new TTS thread for the user input
        user_tts_thread = threading.Thread(target=tts_task, args=(user_input,))
        user_tts_thread.start()

def tts_task(text):
    tts = gTTS(text)
    tts.save("temp.mp3")
    os.system("mpg123 temp.mp3")  # This plays the audio file using mpg123

if __name__ == "__main__":
    # Start the CLI thread
    cli_thread = threading.Thread(target=cli_task)
    cli_thread.start()

    # Wait for the CLI thread to finish (TTS threads will continue running)
    cli_thread.join()

    print("CLI thread has ended. TTS threads are still running.")