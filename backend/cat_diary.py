import os
import base64
from openai import OpenAI
from dotenv import load_dotenv

# Load API Key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Voice style mapping based on tone
VOICE_MAP = {
    "angry": "onyx",
    "annoyed": "onyx",
    "grumpy": "onyx",
    "dramatic": "fable",
    "jealous": "nova",
    "sleepy": "shimmer",
    "lazy": "shimmer",
    "happy": "echo",
    "content": "echo",
    "sarcastic": "fable",
    "cute": "nova",
    "mysterious": "alloy",
    "default": "echo",
}

# Step 1: Detect tone label from image
def detect_cat_tone_from_image(image_path: str) -> str:
    with open(image_path, "rb") as img_file:
        base64_image = base64.b64encode(img_file.read()).decode("utf-8")

    prompt = """
You are a professional cat psychologist. Look at the cat in this photo and describe the tone of voice it would use if it could talk. 
Return just ONE word that describes its speaking tone, such as:
- sarcastic
- sleepy
- angry
- cute
- flirty
- dramatic
- grumpy
- mysterious

Only return ONE word.
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }}
            ]
        }],
        max_tokens=10,
    )
    return response.choices[0].message.content.strip().lower()


# Step 2: Generate storytelling prompt based on image + tone
def generate_prompt_from_image(image_path: str, tone: str) -> str:
    with open(image_path, "rb") as img_file:
        base64_image = base64.b64encode(img_file.read()).decode("utf-8")

    prompt = f"""
You're an imaginative and humorous AI cat. Look at this image of yourself and create a storytelling persona based on your expression and surroundings.
Write a 1-sentence instruction describing your role today. Be creative and tone-aligned.
Tone: {tone}
Example output:
- "You're a lazy prince who just woke up and is annoyed at everything."
- "You're a jealous drama queen cat secretly judging everyone in the room."
Return just the instruction.
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }}
            ]
        }],
        max_tokens=100,
    )
    return response.choices[0].message.content.strip()


# Step 3: Use that prompt to generate diary text
def generate_cat_diary(persona_prompt: str, image_path: str) -> str:
    with open(image_path, "rb") as img_file:
        base64_image = base64.b64encode(img_file.read()).decode("utf-8")

    prompt = f"""
{persona_prompt}

Now write a dramatic, cute, sarcastic, or poetic diary entry (max 80 words) in that voice, from the cat's point of view. Be expressive.
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }}
            ]
        }],
        max_tokens=200,
    )
    return response.choices[0].message.content.strip()


# Step 4: Choose the closest matching voice from tone
def choose_voice_from_tone(tone: str) -> str:
    tone = tone.lower()
    for key in VOICE_MAP:
        if key in tone:
            return VOICE_MAP[key]
    return VOICE_MAP["default"]


# Step 5: Generate audio using selected voice
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


# Step 6: End-to-end generation from image to audio
def generate_cat_diary_all_from_image(image_path: str):
    tone = detect_cat_tone_from_image(image_path)
    persona_prompt = generate_prompt_from_image(image_path, tone)
    diary_text = generate_cat_diary(persona_prompt, image_path)
    voice = choose_voice_from_tone(tone)
    filename = os.path.splitext(os.path.basename(image_path))[0] + "_diary.mp3"
    audio_path = generate_audio(diary_text, voice, filename)

    return {
        "tone": tone,
        "persona": persona_prompt,
        "text": diary_text,
        "voice": voice,
        "audio_path": audio_path
    }
