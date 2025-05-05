# 🐾 CatDiary — Because Your Cat Deserves a Voice (Even If It’s a Little Judgy)

Ever stared into your cat’s eyes and thought,
**“She’s definitely silently judging me... but what exactly is she thinking?”**

CatDiary is an overengineered solution to a deeply unserious problem:
Just upload a photo of your cat.
✨ Behind the scenes, something strange happens.
The app analyzes your cat’s vibe...
🖼️ It looks deep into the image…
📖 Weaves an emotionally charged story based on the scene…
🎙️ Then reads it out loud — in a voice that matches your cat’s mood.

Is your cat a dramatic poet? A grumpy aristocrat? A jealous diva?
You’ll find out — whether you’re ready or not.

Built for Dumb Hackathon. No cats were emotionally harmed.
Sponsored by Stytch... but emotionally powered by tuna withdrawal.

Built for Dumb Hackathon, this app answers the question no one asked:  
**“What is my cat really thinking?”**

---

## Features

- Upload a photo of your cat
- AI detects your cat’s mood and role (e.g. “jealous drama queen”)
- GPT-4o generates a diary entry in that mood
- OpenAI Text-to-Speech (TTS) converts diary into voice with matching tone
- Frontend plays back audio + displays mood and diary

---

## Tech Stack

- OpenAI GPT-4o (Vision + TTS)
- Flask + Python backend
- React (Vite) frontend
- TailwindCSS (or your preferred styling)
- Audio playback via HTML `<audio>` element

---

## How to Build

### 1. Clone & Set Up

```bash
git clone https://github.com/your-username/CatDiary.git
cd CatDiary
```

### 2. Setup Python backend

```bash
cd backend
python -m venv env
env\Scripts\activate       # For Windows
# OR
source env/bin/activate     # For Mac/Linux

pip install -r requirements.txt
```

> 🔐 Make sure to create a `.env` file inside `/backend` with your OpenAI API Key:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
```

---

### 3. Setup React frontend

```bash
cd ../frontend
npm install
```

---

## Run the App

### Start Flask backend

```bash
cd backend
python app.py
```

> Server runs at: `http://localhost:5000`

---

### Start React frontend

```bash
cd frontend
npm run dev
```

> App runs at: `http://localhost:5173`

---

## 📸 API Overview

`POST /api/diary`

| Field | Type | Description |
|-------|------|-------------|
| `image` | `file` | The image file of the cat |

**Returns JSON**:
```json
{
  "tone": "dramatic",
  "persona": "You're a heartbroken bard cat...",
  "text": "In the dim glow of my phone...",
  "voice": "fable",
  "audio_url": "/audio/test_cat3_diary.mp3"
}
```

Audio can be played from:  
`http://localhost:5000/audio/test_cat3_diary.mp3`

---

## Demo Sample Prompt

Upload a cat photo and get:

- Detected Mood: *sarcastic*
- Persona: *You're a drama queen cat judging humans*
- Diary Entry
- Audio playback in matching voice

---

## Credits

Built with ❤️ by Meoww  
Powered by OpenAI + Cat energy
