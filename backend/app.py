from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from cat_diary import generate_cat_diary_all_from_image

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
AUDIO_FOLDER = "audio"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

@app.route("/api/diary", methods=["POST"])
def process_image():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image = request.files["image"]
    if image.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)

    try:
        result = generate_cat_diary_all_from_image(image_path)
        result["audio_url"] = f"/audio/{os.path.basename(result['audio_path'])}"
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_from_directory(AUDIO_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
