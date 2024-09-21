from gm_tts import synthesize_speech, recognize_speech, stop_flag
from file_manager import extract_text_from_pdf
from image_generator import generate_image_from_scene
import threading
from dotenv import load_dotenv
import os

from response_generator import generate_response

# Load environment variables from .env file
load_dotenv()

def gm_loop(game_system, rulebook_text):
    print(f"Starting {game_system} Game Master session...")

    # Introductory message
    intro_message = (
        f"Hello! I am Turing, your Game Master for {game_system}. "
        "What adventure shall we embark on today?"
    )
    threading.Thread(target=synthesize_speech, args=(intro_message,)).start()
    print(intro_message)  # Visible feedback

    while True:
        try:
            user_input = recognize_speech()  # Listen for input
            if user_input:
                stop_flag.set()  # Stop any ongoing TTS playback when the player speaks
                if "exit" in user_input.lower():
                    print("Exiting Game Master session.")
                    break  # Exit condition
                elif "describe" in user_input.lower():
                    # For scene description requests
                    prompt = f"Describe a scene in the {game_system} setting. The player says: {user_input}."
                    mode = "descriptive"
                    response = generate_response(prompt, mode)
                    print(f"Game Master: {response}")

                    # Speak the description
                    stop_flag.clear()
                    threading.Thread(target=synthesize_speech, args=(response,)).start()

                    # Generate an image based on the scene description
                    image_path = generate_image_from_scene(response)
                    print(f"Scene image saved at: {image_path}")
                else:
                    # For general conversation
                    prompt = f"You are a witty game master for {game_system}. The player says: {user_input}. Respond concisely."
                    response = generate_response(prompt)
                    print(f"Game Master: {response}")

                    stop_flag.clear()
                    threading.Thread(target=synthesize_speech, args=(response,)).start()
        except Exception as e:
            print(f"Error: {e}")
            continue



def start_gm():
    print("What game system would you like to play? Cyberpunk RED or D&D 5e?")
    synthesize_speech("What game system would you like to play? Cyberpunk RED or D&D 5e?")

    game_system = input("Enter 'Cyberpunk RED' or 'D&D 5e': ")

    if game_system == "Cyberpunk RED":
        rulebook_path = r"C:\Users\Henrietta\Desktop\CyberpunkRED_Rulebook.pdf"
    elif game_system == "D&D 5e":
        rulebook_path = r"C:\Users\Henrietta\Desktop\DnD5e_Rulebook.pdf"
    else:
        print("Invalid choice. Please select either 'Cyberpunk RED' or 'D&D 5e'.")
        return

    rulebook_text = extract_text_from_pdf(rulebook_path)

    gm_loop(game_system, rulebook_text)


if __name__ == "__main__":
    start_gm()
