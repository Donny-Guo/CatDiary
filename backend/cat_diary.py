import os
from openai import OpenAI
from dotenv import load_dotenv
import requests

# Load your .env file (MUST be in same or parent directory)
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_cat_diary(emotion: str) -> str:
    prompt = f"""
You are a highly expressive cat with a human-level inner monologue. 
Today, you're feeling *{emotion}*. 
Write a short diary entry (max 80 words) capturing your thoughts and emotions. 
You may be dramatic, sarcastic, poetic, or emotionally over-the-top—but still very cat-like.
Example: “My human served me the same can again. I meowed once. Then I meowed twice. Nothing. I might perish.”
Now write today's diary entry:
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
    )
    return response.choices[0].message.content.strip()


def generate_audio(text: str, filename: str = "cat_diary.mp3") -> str:
    # Make sure output folder exists
    os.makedirs("audio", exist_ok=True)
    output_path = os.path.join("audio", filename)

    # Use OpenAI TTS
    response = client.audio.speech.create(
        model="tts-1",
        voice="onyx",  # Try others: alloy, echo, fable, nova, shimmer
        input=text,
        response_format="mp3",
    )

    # Save the audio
    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path


def generate_cat_audio_diary(emotion: str):
    text = generate_cat_diary(emotion)
    safe_filename = f"{emotion.replace(' ', '_').lower()}_diary.mp3"
    audio_path = generate_audio(text, safe_filename)
    return text, audio_path
