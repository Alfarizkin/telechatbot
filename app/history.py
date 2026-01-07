import json
import os
from typing import List, Dict

BASE_PATH = "data/chats"
os.makedirs(BASE_PATH, exist_ok=True)

def _chat_filename(user_char: str, ai_char: str) -> str:
    name = f"{user_char}__{ai_char}.json"
    return os.path.join(BASE_PATH, name)

def load_history(user_char: str, ai_char: str) -> List[Dict]:
    path = _chat_filename(user_char, ai_char)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_history(user_char: str, ai_char: str, history: List[Dict]):
    path = _chat_filename(user_char, ai_char)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
