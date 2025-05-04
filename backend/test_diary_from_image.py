from cat_diary import generate_cat_audio_diary_from_image

image_path = "backend/test_cat.jpg"  # Replace with your uploaded image filename

text, audio_path = generate_cat_audio_diary_from_image(image_path)

print("=== Cat Diary (Generated from Image) ===")
print(text)
print(f"Audio saved at: {audio_path}")
