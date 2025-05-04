from flask import Flask, request, jsonify, render_template
from datetime import date
import os, json

app = Flask(
    __name__,
    static_folder="static",         # built by Vite
    template_folder="templates"     # index.html loaded here
)

UPLOAD_FOLDER = os.path.join(app.static_folder, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/diary', methods=['POST'])
def save_diary():
    mood = request.form.get('mood')
    text = request.form.get('text')
    image = request.files.get('image')
    audio = request.files.get('audio')

    entry = {
        "date": str(date.today()),
        "mood": mood,
        "text": text
    }

    if image:
        image_path = os.path.join("uploads", image.filename)
        image.save(os.path.join(UPLOAD_FOLDER, image.filename))
        entry["image"] = image_path

    if audio:
        audio_path = os.path.join("uploads", audio.filename)
        audio.save(os.path.join(UPLOAD_FOLDER, audio.filename))
        entry["audio"] = audio_path

    with open(f"diary_{date.today()}.json", "w") as f:
        json.dump(entry, f)

    return jsonify({"message": "Diary saved!"})

@app.route('/api/diary', methods=['GET'])
def get_diary():
    try:
        with open(f"diary_{date.today()}.json") as f:
            return jsonify(json.load(f))
    except FileNotFoundError:
        return jsonify({"message": "No entry found."}), 404

if __name__ == '__main__':
    app.run(debug=True)
