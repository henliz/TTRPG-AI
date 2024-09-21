from diffusers import StableDiffusionPipeline
import torch
from gm_tts import synthesize_speech  # The text-to-speech function

# Load the model
pipe = StableDiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-2-1-base",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
).to("cuda" if torch.cuda.is_available() else "cpu")


def convert_description_to_prompt(description):
    # Simplified key details for image generation
    bullet_points = [
        "Bustling village square with market stalls.",
        "Majestic oak tree at the center.",
        "Mysterious woman in white robes with a raven perched on her cane.",
        "Villagers speaking in hushed tones."
    ]
    return ". ".join(bullet_points)


def generate_image_from_scene(description):
    # Concise prompt for image generation
    prompt = convert_description_to_prompt(description)

    print(f"Generating image for prompt: {prompt}")

    # Generate the image
    image = pipe(prompt).images[0]

    # Save and return the image
    image_path = "generated_image.png"
    image.save(image_path)
    print(f"Image generated and saved to '{image_path}'")

    return image_path


# Example function to describe the scene and generate the image
def describe_and_generate(scene_description):
    # Speak the full, rich description aloud
    synthesize_speech(scene_description)

    # Generate the image based on the concise prompt
    image_path = generate_image_from_scene(scene_description)

    return image_path

#end of file
