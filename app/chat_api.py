from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from .ai_client import ask_ai
from .history import load_history, save_history

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    user_character: str
    ai_character: str
    user_prompt: str

class ChatResponse(BaseModel):
    reply: str
    history: List[dict]

@router.post("/", response_model=ChatResponse)
async def chat(req: ChatRequest):
    history = load_history(req.user_character, req.ai_character)

    # system prompt (role karakter)
    system_prompt = {
        "role": "system",
        "content": f"""
You are roleplaying as character '{req.ai_character}'.
The user is roleplaying as '{req.user_character}'.
Stay in character. Do not break roleplay.
"""
    }

    messages = [system_prompt] + history
    messages.append({"role": "user", "content": req.user_prompt})

    ai_reply = await ask_ai(messages)

    history.append({"role": "user", "content": req.user_prompt})
    history.append({"role": "assistant", "content": ai_reply})

    save_history(req.user_character, req.ai_character, history)

    return {
        "reply": ai_reply,
        "history": history
    }
