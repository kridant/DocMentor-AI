from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Read Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY is None:
    raise ValueError("Gemini API Key not found! Please check your .env file.")