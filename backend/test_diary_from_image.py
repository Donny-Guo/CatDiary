from cat_diary import generate_cat_diary_all_from_image

image_path = "backend/test_cat.jpg"

result = generate_cat_diary_all_from_image(image_path)

print("=== Detected Emotion ===")
print(result["emotion"])
print("\n=== AI Cat Diary ===")
print(result["text"])
print(f"\n🎧 Audio saved at: {result['audio_path']}")
