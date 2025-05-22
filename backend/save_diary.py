from supabase import create_client
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_diary_to_supabase(user_id, image_url, diary_text, audio_url):
    print("🟡 DEBUG: Preparing to save to Supabase...")
    print("user_id:", user_id)
    print("image_url:", image_url)
    print("diary_text:", diary_text)
    print("audio_url:", audio_url)
    print("created_at:", datetime.utcnow().isoformat())

    try:
        response = supabase.table("cat_diary").insert({
            "user_id": user_id,
            "image_url": image_url,
            "diary_text": diary_text,
            "audio_url": audio_url,
            "created_at": datetime.utcnow().isoformat()
        }).execute()

        if response.get("error"):
            print("❌ Failed to save diary:", response["error"]["message"])
        else:
            print("✅ Supabase response:", response)
            print("✅ Diary saved to Supabase!")
    except Exception as e:
        print("❌ Exception while saving diary:", e)
