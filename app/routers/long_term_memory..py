from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.long_term_memory import LongTermMemoryRequest, AddMemoryResponse
from ..services.long_term_memory import LongTermMemoryService
from ..cores.exception import DatabaseError, ChatServiceError, AIServiceError

from ..cores.database import get_db

router = APIRouter (prefix="/memory", tags=["Memory"])

@router.post(
    path="/",
    response_model=AddMemoryResponse
)
async def add_memory(
    data: LongTermMemoryRequest,
    db: AsyncSession = Depends(get_db)
):
    service = LongTermMemoryService(db)
    try:
        result = await service.add_memory(
            chat_id=data.chat_id,
            content=data.content
        )
        return result
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail={e})