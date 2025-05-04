import os
import base64
from openai import OpenAI
from dotenv import load_dotenv

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# === 🖼️ Step 1: Generate diary text from image ===
def generate_cat_diary_from_image(image_path: str) -> str:
    with open(image_path, "rb") as img_file:
        base64_image = base64.b64encode(img_file.read()).decode("utf-8")

    prompt = """
You are a cat. You can see this image as if it's your own reflection or a snapshot of your current life. 
Describe your inner thoughts and feelings, and write a short diary entry (max 80 words) in a dramatic, sarcastic, or poetic tone.

Speak like a cat with a personality. Pretend this picture represents your moment today.
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }}
            ]}
        ],
        max_tokens=200
    )

    return response.choices[0].message.content.strip()

# === 🔊 Step 2: Generate speech from text ===
def generate_audio(text: str, filename: str = "cat_diary.mp3") -> str:
    os.makedirs("audio", exist_ok=True)
    output_path = os.path.join("audio", filename)

    response = client.audio.speech.create(
        model="tts-1",
        voice="onyx",  # You can try nova, fable, echo, shimmer, alloy
        input=text,
        response_format="mp3",
    )

    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path

# === 🧩 Wrapper: from image to full audio diary ===
def generate_cat_audio_diary_from_image(image_path: str):
    text = generate_cat_diary_from_image(image_path)
    filename = os.path.splitext(os.path.basename(image_path))[0] + "_diary.mp3"
    audio_path = generate_audio(text, filename)
    return text, audio_path
