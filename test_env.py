import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env", override=True)

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    print("SUCCESS: Gemini API key loaded!")
    print("Key length:", len(api_key))
else:
    print("ERROR: Gemini API key not found!")