import os
from dotenv import load_dotenv

# Load environment variables from .env file automatically
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gemini-2.5-flash")

AMADUES_CLIENT_ID = os.getenv("AMADUES_CLIENT_ID")
AMADUES_CLIENT_SECRET = os.getenv("AMADUES_CLIENT_SECRET")
