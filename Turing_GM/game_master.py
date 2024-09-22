import threading
from pdf_handler import PDFStoryHandler
from story_manager import StoryManager
from gm_tts import synthesize_speech, recognize_speech, stop_flag
from file_manager import extract_text_from_pdf  # Make sure this line is included
from dotenv import load_dotenv
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

def gm_loop(game_system, rulebook_text):
    pdf_path = r"C:\Users\Henrietta\PycharmProjects\TTRPG-AI\Campaigns\DnD\curse_of_strahd.pdf"
    pdf_handler = PDFStoryHandler(pdf_path)
    story_manager = StoryManager(game_system)

    print(f"Starting {game_system} Game Master session...")
    intro_message = f"Hello! I am Turing, your Game Master for {game_system}. What adventure shall we embark on today?"
    threading.Thread(target=synthesize_speech, args=(intro_message,)).start()
    print(intro_message)

    while True:
        try:
            user_input = recognize_speech()  # Listen for input
            if user_input:
                if "exit" in user_input.lower():
                    print("Exiting Game Master session.")
                    break
                elif "describe" in user_input.lower():
                    # Handle scene description requests
                    prompt = f"Describe a scene in the {game_system} setting. The player says: {user_input}."
                    response = story_manager.generate_response(prompt, mode="descriptive")
                    print(f"Game Master: {response}")
                    threading.Thread(target=synthesize_speech, args=(response,)).start()

                elif any(word in user_input.lower() for word in ["strahd", "barovia", "item"]):
                    # Fetch info from the PDF for Curse of Strahd module
                    response = story_manager.generate_response(user_input)
                    print(f"Game Master: {response}")
                    threading.Thread(target=synthesize_speech, args=(response,)).start()

                else:
                    # General conversation or instructions
                    prompt = f"You are a witty game master for {game_system}. The player says: {user_input}. Respond concisely."
                    response = story_manager.generate_response(prompt)
                    print(f"Game Master: {response}")
                    threading.Thread(target=synthesize_speech, args=(response,)).start()

        except Exception as e:
            print(f"Error: {e}")
            continue


def start_gm():
    # Start session and ask for game selection
    synthesize_speech("Hi, I'm Turing. Do you want to play Cyberpunk RED or D&D 5e?")
    print("What game system would you like to play? Cyberpunk RED or D&D 5e?")

    game_system = recognize_speech()

    if "cyberpunk" in game_system.lower():
        rulebook_path = "C:/Users/Henrietta/Desktop/CyberpunkRED_Rulebook.pdf"
        game_system = "Cyberpunk RED"
    elif "d&d" in game_system.lower() or "dungeons" in game_system.lower():
        rulebook_path = "C:/Users/Henrietta/Desktop/DnD5e_Rulebook.pdf"
        game_system = "D&D 5e"
    else:
        synthesize_speech("Sorry, I didn't catch that. Please say either Cyberpunk or D&D.")
        return

    rulebook_text = extract_text_from_pdf(rulebook_path)
    gm_loop(game_system, rulebook_text)

if __name__ == "__main__":
    start_gm()
