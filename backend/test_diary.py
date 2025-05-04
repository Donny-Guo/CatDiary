# test_diary.py
from cat_diary import generate_cat_audio_diary

# 模擬照片分析後得到的情緒
detected_emotion = "grumpy"

text, audio_path = generate_cat_audio_diary(detected_emotion)

print("=== AI-Generated Cat Diary ===")
print(text)
print(f"Audio saved at: {audio_path}")
