from pydantic import BaseModel
from typing import Optional
from typing import List

class ChatRequest(BaseModel):
    chat_id: str
    ai_name: str
    ai_identity: str
    ai_rules: str
    user_prompt: str