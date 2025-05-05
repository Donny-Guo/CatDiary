# Backend - CatDiary API

This is the backend service for **CatDiary**, built using Flask and OpenAI's GPT-4o + TTS API.

It receives cat photos, analyzes the image, generates a diary entry based on the cat's detected tone, and returns both text and generated audio.

---

## How It Works

1. Receive an image via POST request.
2. Use GPT-4o (with vision) to analyze the cat's expression.
3. Detect a matching emotional tone (e.g. sarcastic, dramatic).
4. Generate a role/persona and diary-style monologue.
5. Use OpenAI TTS (Text-to-Speech) to turn the diary into a voice message.
6. Return all the information as JSON + serve the audio file.

---

## Requirements

- Python 3.9+
- OpenAI API key

---

## Setup

```bash
cd backend
python -m venv env
env\Scripts\activate       # Windows
# OR
source env/bin/activate     # macOS/Linux

pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in `/backend` folder:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## Run the Server

```bash
python app.py
```

Server will be running at:

```
http://localhost:5000
```

---

## API Endpoint

### POST `/api/diary`

Upload an image file with key: `image`

#### Example Response:

```json
{
  "tone": "dramatic",
  "persona": "You're a heartbroken bard cat...",
  "text": "In the dim glow of my phone...",
  "voice": "fable",
  "audio_url": "/audio/test_cat_diary.mp3"
}
```

---

### GET `/audio/<filename>`

Serves the audio file associated with the diary.

---

## File Structure Overview

```
backend/
├── app.py              # Main Flask app
├── cat_diary.py        # Core logic for image analysis, diary + audio generation
├── uploads/            # Uploaded images
├── audio/              # Generated audio files
├── .env                # Your OpenAI API key
└── requirements.txt    # Python dependencies
```

---

## Credits

Part of the CatDiary project, built with OpenAI, Flask, and too much love for cats 😽
