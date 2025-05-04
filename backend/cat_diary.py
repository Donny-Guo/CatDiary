import os
import base64
from openai import OpenAI
from dotenv import load_dotenv

# Load API Key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Step 1️⃣: Detect cat emotion from image
def detect_cat_emotion_from_image(image_path: str) -> str:
    with open(image_path, "rb") as img_file:
        base64_image = base64.b64encode(img_file.read()).decode("utf-8")

    prompt = """
You are an expert cat psychologist. Look at the photo and describe the cat's emotion in one or two English words, such as:
- sleepy
- annoyed
- dramatic
- content
- jealous
- angry
- surprised
Only return the emotion words, no explanation.
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
        max_tokens=20
    )

    return response.choices[0].message.content.strip().lower()


# Step 2️⃣: Generate diary text using emotion + image
def generate_cat_diary(emotion: str, image_path: str) -> str:
    with open(image_path, "rb") as img_file:
        base64_image = base64.b64encode(img_file.read()).decode("utf-8")

    prompt = f"""
You are a dramatic, poetic, or sarcastic cat. Based on this image and the fact that you feel *{emotion}*, write a short diary entry (max 80 words) from your perspective. Be creative and emotionally expressive.
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


# Step 3️⃣: Match emotion to OpenAI voice
def choose_voice_from_emotion(emotion: str) -> str:
    emotion = emotion.lower()
    if "angry" in emotion or "annoyed" in emotion:
        return "onyx"
    elif "dramatic" in emotion:
        return "fable"
    elif "jealous" in emotion:
        return "nova"
    elif "sleepy" in emotion:
        return "shimmer"
    elif "happy" in emotion or "content" in emotion:
        return "echo"
    else:
        return "alloy"  # Default fallback


# Step 4️⃣: Generate audio from text
def generate_audio(text: str, voice: str, filename: str = "cat_diary.mp3") -> str:
    os.makedirs("audio", exist_ok=True)
    output_path = os.path.join("audio", filename)

    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text,
        response_format="mp3",
    )

    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path


# Step 5️⃣: Full pipeline from image → emotion → text → audio
def generate_cat_diary_all_from_image(image_path: str):
    emotion = detect_cat_emotion_from_image(image_path)
    text = generate_cat_diary(emotion, image_path)
    voice = choose_voice_from_emotion(emotion)

    filename = os.path.splitext(os.path.basename(image_path))[0] + "_diary.mp3"
    audio_path = generate_audio(text, voice, filename)

    return {
        "emotion": emotion,
        "text": text,
        "audio_path": audio_path
    }
