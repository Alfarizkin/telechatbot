import json
import os
from typing import List, Dict

BASE_PATH = "data/chats"
os.makedirs(BASE_PATH, exist_ok=True)

def _get_path(chat_id: str) -> str:
    return os.path.join(BASE_PATH, f"chat_{chat_id}.json")

def load_history(chat_id: str) -> List[Dict]:
    path = _get_path(chat_id)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return []

def save_history(chat_id: str, history: List[Dict]):
    path = _get_path(chat_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
