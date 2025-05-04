from cat_diary import generate_cat_audio_diary

detected_emotion = "dramatic"  # Or "grumpy", "jealous", "sleepy" etc.
text, audio_path = generate_cat_audio_diary(detected_emotion)

print("=== AI-Generated Cat Diary ===")
print(text)
print(f"Audio saved at: {audio_path}")
