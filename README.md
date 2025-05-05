# 🐾 CatDiary: AI-Powered Cat Mood Translator

CatDiary lets you upload a photo of your cat and receive a hilariously accurate AI-generated diary entry — complete with a dramatic or grumpy voiceover.

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
