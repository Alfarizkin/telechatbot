from pydantic import BaseModel
from typing import Optional
from typing import List
from datetime import datetime

class LongTermMemorySchema(BaseModel):

    chat_id: str
    content: str
    embedding: List[float]
    created_at: datetime | None = None

    model_config = {
        "from_attributes": True
    }

class LongTermMemoryRequest(BaseModel):
    chat_id: str
    content: str

class AddMemoryResponse(BaseModel):
    saved: bool
    memory: Optional[LongTermMemorySchema] = None
    reason: Optional[str] = None