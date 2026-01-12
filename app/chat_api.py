from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from .ai_client import ask_ai
from .history import load_history, save_history

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    chat_id: str
    ai_name: str
    ai_identity: str
    ai_rules: str
    user_prompt: str

class ChatResponse(BaseModel):
    reply: str
    history: List[dict]

@router.post("/", response_model=ChatResponse)
async def chat(req: ChatRequest):
    history = load_history(req.chat_id)

    system_content = (
        f"Roleplay Identity: {req.ai_identity}\n"
        f"Behavioral Rules: {req.ai_rules}\n"
        f"Current Persona: You are {req.ai_name}. Stay in character."
    )

    system_prompt = {"role": "system", "content": system_content}

    messages = [system_prompt] + history[-15:]
    messages.append({"role": "user", "content": req.user_prompt})

    ai_reply = await ask_ai(messages)

    history.append({"role": "user", "content": req.user_prompt})
    history.append({"role": "assistant", "content": ai_reply})

    save_history(req.chat_id, history)

    return {
        "reply": ai_reply,
        "history": history
    }
