import os
from dotenv import load_dotenv
import openai
from chattts import ChatTTS
import torchaudio

# Load OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load ChatTTS model once
tts_model = ChatTTS.load_from_pretrained()

# Accepts an emotion string (e.g. "sleepy", "grumpy") and generates a diary entry
def generate_cat_diary(emotion: str) -> str:
    prompt = f"""
You are a highly expressive cat with a human-level inner monologue. 
Today, you're feeling *{emotion}*. 
Write a short diary entry (max 80 words) capturing your thoughts and emotions. 
You may be dramatic, sarcastic, poetic, or emotionally over-the-top—but still very cat-like.
Example: “My human served me the same can again. I meowed once. Then I meowed twice. Nothing. I might perish.”
Now write today's diary entry:
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
    )
    return response['choices'][0]['message']['content'].strip()

# Converts text into audio using ChatTTS and returns the audio file path
def generate_audio(text: str, filename: str = "cat_diary.wav") -> str:
    wav, sr = tts_model.synthesize(text, speaker="emo-cat")
    os.makedirs("audio", exist_ok=True)
    output_path = os.path.join("audio", filename)
    torchaudio.save(output_path, wav.unsqueeze(0), sr)
    return output_path

# Combines diary + audio generation into a single call
def generate_cat_audio_diary(emotion: str):
    text = generate_cat_diary(emotion)
    sanitized = emotion.replace(" ", "_").lower()
    filename = f"{sanitized}_diary.wav"
    audio_path = generate_audio(text, filename)
    return text, audio_path
