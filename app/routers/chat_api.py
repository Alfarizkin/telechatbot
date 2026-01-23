from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.chat_response import ChatResponse
from ..schemas.chat_request import ChatRequest
from ..schemas.chat_history import ChatHistoryResponse
from ..services.chat_service import ChatService
from ..cores.exception import DatabaseError, ChatServiceError, AIServiceError

from ..cores.database import get_db

router_chat = APIRouter(prefix="/chats", tags=["Chat"])

@router_chat.post(
        path="/",
        response_model=ChatResponse)
async def chat(
    data: ChatRequest,
    db: AsyncSession = Depends(get_db)
    ):
    service = ChatService(db)
    try:
        result = await service.handle_chat(
            chat_id=data.chat_id,
            ai_name=data.ai_name,
            ai_identity=data.ai_identity,
            ai_rules=data.ai_rules,
            user_prompt=data.user_prompt
        )
        
        return {"reply" : result}
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=e)
    except ChatServiceError as e:
        raise HTTPException(status_code=500, detail=e)
    except AIServiceError as e:
        raise HTTPException(status_code=502, detail=e)

@router_chat.get(
    path="/{chat_id}/messages",
    response_model=ChatHistoryResponse
)
async def get_history(
    chat_id: str,
    db:AsyncSession = Depends(get_db)
    ):
    service = ChatService(db)
    try:
        result = await service.get_history_chat(chat_id)
        return {"messages": result}
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=e)
