import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
