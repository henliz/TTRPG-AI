import threading  # For running tasks concurrently
from google.cloud import texttospeech  # Google Cloud Text-to-Speech API
from playsound import playsound  # For audio playback
import speech_recognition as sr
from dotenv import load_dotenv
import os

# Initialize the stop_flag
stop_flag = threading.Event()

# Setup Google Cloud Text-to-Speech client
client = texttospeech.TextToSpeechClient()


def synthesize_speech(text):
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D"  # Adjust as needed
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Save the audio file
    audio_path = "output.mp3"
    with open(audio_path, "wb") as out:
        out.write(response.audio_content)
        print("Audio content written to 'output.mp3'")

    # Play the audio
    play_audio(audio_path)


def play_audio(audio_path):
    global stop_flag
    stop_flag.clear()  # Reset stop flag before playing
    try:
        playsound(audio_path)
    except Exception as e:
        print(f"Error during playback: {e}")


def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for speech input...")
        try:
            audio = recognizer.listen(source, timeout=10)  # Add timeout
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.WaitTimeoutError:
            print("Timeout: No speech detected.")
            return ""
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return ""

