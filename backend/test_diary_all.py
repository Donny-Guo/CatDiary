from cat_diary import generate_cat_diary_all_from_image

result = generate_cat_diary_all_from_image("backend/test_cat2.jpg")

print("🐾 Detected Tone:", result["tone"])
print("🎭 Persona Prompt:", result["persona"])
print("\n📖 Diary:\n", result["text"])
print("🎧 Voice Used:", result["voice"])
print("📁 Audio Saved At:", result["audio_path"])
