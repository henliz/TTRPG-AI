import os
import cohere

# Setup Cohere API Key
cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))

conversation_history = []  # A list to store the history of prompts and responses

def generate_response(prompt, mode="concise"):
    global conversation_history
    # Add the current prompt to the history
    conversation_history.append(f"Player: {prompt}")

    # Combine previous context into the current prompt
    full_prompt = "\n".join(conversation_history) + f"\nGame Master:"

    if mode == "descriptive":
        temperature = 0.8
        max_tokens = 300
    else:
        temperature = 0.7
        max_tokens = 150

    response = cohere_client.generate(
        model='command',
        prompt=full_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    # Save the AI's response to the history
    conversation_history.append(f"Game Master: {response.generations[0].text.strip()}")

    return response.generations[0].text.strip()

