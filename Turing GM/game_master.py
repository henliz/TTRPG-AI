from gm_tts import synthesize_speech, recognize_speech, stop_flag
from response_generator import generate_response
from file_manager import extract_text_from_pdf
import threading
import random

# Store conversation history for context
conversation_history = []


def gm_loop(game_system, rulebook_text):
    print(f"Starting {game_system} Game Master session...")

    # Introductory blurb
    intro_message = (
        f"Hey there! It's Turing, your trusty Game Master. "
        "Are you ready to dive into some epic adventures? What would you like to do?"
    )
    threading.Thread(target=synthesize_speech, args=(intro_message,)).start()  # Run TTS in a separate thread
    print(intro_message)

    while True:
        user_input = recognize_speech()

        if user_input:
            stop_flag.set()  # Stop ongoing TTS playback when the player starts speaking

            # Define the prompt for the Game Master
            prompt = f"The player asks: '{user_input}'. Respond in character."

            # Check for specific interactions
            if "necromancer" in user_input.lower() or "barkeep" in user_input.lower():
                # Prompt for a charisma check
                charisma_check = random.randint(1, 20) + 2  # Example: Add a bonus to the roll
                response = f"You notice the barkeep is not telling you everything... Make a Charisma check!"
                print(f"Game Master: {response}")
                synthesize_speech(response)

                # Here, you could ask for player input for the skill check
                skill_check_input = recognize_speech()
                if "roll" in skill_check_input.lower() or "check" in skill_check_input.lower():
                    # Assume player decides to roll
                    if charisma_check >= 15:  # Example success threshold
                        response = "The barkeep relaxes a bit and shares more details about the necromancer..."
                    else:
                        response = "The barkeep remains tight-lipped and gives you a wary look."
                    print(f"Game Master: {response}")
                    synthesize_speech(response)
                    continue  # Continue to the next interaction

            # Continue normal conversation
            response = generate_response(prompt, "concise")
            print(f"Game Master: {response}")

            # Restart TTS for the new response
            stop_flag.clear()
            threading.Thread(target=synthesize_speech, args=(response,)).start()


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
    print(rulebook_text)  # Optionally use this text if needed

    gm_loop(game_system, rulebook_text)


if __name__ == "__main__":
    start_gm()


