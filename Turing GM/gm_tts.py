import os
import time
from google.cloud import texttospeech  # Google Cloud Text-to-Speech API
import speech_recognition as sr  # For speech recognition
from playsound import playsound  # For playing audio files
import threading  # For running tasks concurrently
from dotenv import load_dotenv  # For loading environment variables from .env file
from pydub import AudioSegment
from pydub.playback import play


# Load environment variables from .env
load_dotenv()

# Setup Google Cloud Text-to-Speech client
client = texttospeech.TextToSpeechClient()

# Flag to stop TTS playback
stop_flag = threading.Event()

def synthesize_speech(text):
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D"  # Use a neural voice for more natural sound
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.1,
        pitch=2.0  # Adjust pitch
    )

    # Generate a unique filename
    audio_path = f"output_{int(time.time())}.mp3"  # Use timestamp for uniqueness
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(audio_path, "wb") as out:
        out.write(response.audio_content)
        print(f"Audio content written to '{audio_path}'")

    # Play the generated speech audio
    audio = AudioSegment.from_mp3(audio_path)
    play(audio)

    # Optional: Delete the audio file after playback
    os.remove(audio_path)


def play_audio(audio_path):
    global stop_flag
    # Play the audio using playsound
    if not stop_flag.is_set():
        playsound(audio_path)

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=10)  # Add a timeout to prevent hanging
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.WaitTimeoutError:
            print("Timeout: You didn't speak in time.")
            return ""
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return ""
