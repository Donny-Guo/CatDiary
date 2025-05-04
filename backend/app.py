from flask import Flask, request, jsonify, render_template
from flask import redirect, url_for, session
from datetime import date
import os, json, dotenv, datetime
from stytch import Client
from stytch.core.response_base import StytchError


# load the .env file
dotenv.load_dotenv()

# Load stytch client
stytch_client = Client(
  project_id=os.getenv("STYTCH_PROJECT_ID"),
  secret=os.getenv("STYTCH_SECRET"),
  environment="test"
)

def create_user_directories(user_id):
    base_path = os.path.join('diary', user_id)
    audio_path = os.path.join(base_path, 'audio')
    os.makedirs(audio_path, exist_ok=True)
    return base_path, audio_path

app = Flask(
    __name__,
    static_folder="static",         # built by Vite
    template_folder="templates"     # index.html loaded here
)
app.secret_key = 'supersecret'

UPLOAD_FOLDER = os.path.join(app.static_folder, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    response = stytch_client.magic_links.email.login_or_create(email=email)
    # Send the magic link to the user's email
    return 'Magic link sent to your email.'

@app.route('/authenticate', methods=['GET'])
def authenticate():
    token = request.args.get('token')
    response = stytch_client.magic_links.authenticate(token=token)
    user_id = response.user_id
    session['user_id'] = user_id
    create_user_directories(user_id)
    return redirect(url_for('dashboard'))


# Fake login for dev (replace with Stytch later)
@app.before_request
def mock_login():
    session['user_id'] = 'user123'  # ← mock a logged-in user

def create_user_dirs(user_id):
    base_path = os.path.join('diary', user_id)
    os.makedirs(os.path.join(base_path, 'images'), exist_ok=True)
    os.makedirs(os.path.join(base_path, 'audio'), exist_ok=True)
    return base_path

@app.route('/api/diary', methods=['POST'])
def save_diary():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    base_path = create_user_dirs(user_id)
    image_folder = os.path.join(base_path, 'images')
    audio_folder = os.path.join(base_path, 'audio')
    diary_file = os.path.join(base_path, 'diary.json')

    mood = request.form.get('mood')
    text = request.form.get('text')
    image = request.files.get('image')
    audio = request.files.get('audio')

    timestamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')

    entry = {
        "date": str(date.today()),
        "mood": mood,
        "text": text
    }

    if image:
        ext = os.path.splitext(image.filename)[-1]
        image_filename = f"{timestamp}{ext}"
        image_path = os.path.join(image_folder, image_filename)
        image.save(image_path)
        entry['image'] = f"images/{image_filename}"

    if audio:
        ext = os.path.splitext(audio.filename)[-1]
        audio_filename = f"{timestamp}{ext}"
        audio_path = os.path.join(audio_folder, audio_filename)
        audio.save(audio_path)
        entry['audio'] = f"audio/{audio_filename}"

    # Load or initialize diary
    diary_data = []
    if os.path.exists(diary_file):
        with open(diary_file, 'r') as f:
            diary_data = json.load(f)

    # Update today’s entry
    diary_data = [e for e in diary_data if e['date'] != entry['date']]
    diary_data.append(entry)

    with open(diary_file, 'w') as f:
        json.dump(diary_data, f, indent=2)

    return jsonify({"message": "Diary saved!"})

@app.route('/api/diary', methods=['GET'])
def get_diary():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    diary_file = os.path.join('diary', user_id, 'diary.json')
    if os.path.exists(diary_file):
        with open(diary_file, 'r') as f:
            return jsonify(json.load(f))
    return jsonify([])


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
