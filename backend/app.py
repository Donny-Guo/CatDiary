from flask import Flask, request, jsonify, render_template
from flask import redirect, url_for, session
from flask import send_from_directory
from datetime import date, datetime
import os, json, dotenv
from stytch import Client
from stytch.core.response_base import StytchError
from cat_diary import generate_cat_diary_all_from_image

# load the .env file
dotenv.load_dotenv()

# Load stytch client
stytch_client = Client(
  project_id=os.getenv("STYTCH_PROJECT_ID"),
  secret=os.getenv("STYTCH_SECRET"),
  environment="test"
)

app = Flask(
    __name__,
    static_folder="static",         # built by Vite
    template_folder="templates"     # index.html loaded here
)
app.secret_key = 'supersecret'

UPLOAD_FOLDER = os.path.join(app.static_folder, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.route('/')
# def index():
#     return render_template('index.html')
@app.route('/')
def index():
    user_id = session.get('user_id')
    vite_dev = os.getenv("FLASK_ENV") == "development"
    return render_template('index.html', user_id=user_id, vite_dev=vite_dev)


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    response = stytch_client.magic_links.email.login_or_create(email=email)
    # Send the magic link to the user's email
    return 'Magic link sent to your email.'

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route('/authenticate', methods=['GET'])
def authenticate():
    token = request.args.get('token')
    try:
        response = stytch_client.magic_links.authenticate(token=token)
        user_id = response.user_id
        session['user_id'] = user_id
        create_user_dirs(user_id)
        return redirect(url_for('index'))  # or a dashboard page
    except StytchError as e:
        return f"Authentication failed: {e}", 401



# # Fake login for dev (replace with Stytch later)
# @app.before_request
# def mock_login():
#     session['user_id'] = 'user123'  # ← mock a logged-in user

def create_user_dirs(user_id):
    base_path = os.path.join('../diary', user_id)
    os.makedirs(os.path.join(base_path, 'images'), exist_ok=True)
    os.makedirs(os.path.join(base_path, 'audio'), exist_ok=True)
    return base_path


@app.route('/audio/<filename>')
def serve_audio(filename):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    audio_folder = os.path.join('../diary', user_id, 'audio')
    full_path = os.path.join(audio_folder, filename)

    print("[DEBUG] Trying to serve:", full_path)

    if not os.path.exists(full_path):
        print("[ERROR] File does not exist:", full_path)
        return jsonify({"error": "File not found"}), 404

    return send_from_directory(audio_folder, filename)

@app.route('/test-audio/<filename>')
def test_audio(filename):
    print(f"[debug] filename: {filename}")
    path ='diary/user123/audio' 
    return send_from_directory(path, filename)


@app.route('/api/generate', methods=['POST'])
def generate_diary_from_image():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    base_path = create_user_dirs(user_id)
    image_folder = os.path.join(base_path, 'images')
    audio_folder = os.path.join(base_path, 'audio')

    image = request.files.get('image')
    if not image:
        return jsonify({"error": "Image file is required"}), 400

    timestamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
    ext = os.path.splitext(image.filename)[-1] or ".jpg"
    image_filename = f"{timestamp}{ext}"
    image_path = os.path.join(image_folder, image_filename)
    image.save(image_path)

    # Define where to save generated audio
    audio_filename = f"{timestamp}_diary.mp3"
    audio_path = os.path.join(audio_folder, audio_filename)

    try:
        result = generate_cat_diary_all_from_image(image_path, audio_path)
        # result['image'] = f"images/{image_filename}"
        result['image'] = image_path
        result['audio_path'] = audio_filename
        return jsonify(result)
    except Exception as e:
        print("Diary generation failed:", e)
        return jsonify({
            "text": '',
            "audio_path": '',
            "tone": '',
            "persona": '',
            "voice": '',
            "error": str(e)
        }), 500


@app.route('/api/diary', methods=['POST'])
def save_generated_diary():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    base_path = create_user_dirs(user_id)
    diary_file = os.path.join(base_path, 'diary.json')

    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    entry = {
        "date": str(date.today()),
        "text": data.get('text', ''),
        "tone": data.get('tone', ''),
        "persona": data.get('persona', ''),
        "voice": data.get('voice', ''),
        "audio_path": data.get('audio_path', '')
    }

    diary_data = []
    if os.path.exists(diary_file):
        with open(diary_file, 'r') as f:
            diary_data = json.load(f)

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
    app.run(host='localhost', port=3000, debug=True)
