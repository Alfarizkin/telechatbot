from pydantic import BaseModel
from typing import Optional
from typing import List

class ChatResponse(BaseModel):
    reply: str
    history: List[dict]