from pydantic import BaseModel
from datetime import datetime

class ChatHistoryRequest(BaseModel):
    chat_id: str

class ChatMessageSchema(BaseModel):
    role: str
    content: str
    created_at: datetime | None = None

    model_config = {
        "from_attributes": True
    }

class ChatHistoryResponse(BaseModel):
    messages: list[ChatMessageSchema]