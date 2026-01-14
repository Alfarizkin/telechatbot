from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from ..models.long_term_memory import LongTermMemory
from sentence_transformers import SentenceTransformer

class LongTermMemoryRepository:
    def __init__(
            self,
            session: AsyncSession
            ):
        self.session = session

    async def add_memory(
        self,
        chat_id: str,
        content: str,
        embedding: List[float]
    ):
        msg = LongTermMemory(
            chat_id=chat_id,
            content=content,
            embedding=embedding
        )
        self.session.add(msg)
        await self.session.commit()
        await self.session.refresh(msg)
        return msg
    
    async def get_recent_memory(
        self,
        chat_id:str,
        limit: int = 10
    ) -> List[LongTermMemory]:
        stmt = (
            select(LongTermMemory)
            .where(LongTermMemory.chat_id == chat_id)
            .order_by(LongTermMemory.created_at.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(reversed(result.scalars().all()))
    
    async def search_similar_memory(
        self,
        chat_id:str,
        embedding: List[float],
        top_k: int = 5
    ) -> List[LongTermMemory]:
        stmt = (
            select(LongTermMemory)
            .where(LongTermMemory.chat_id==chat_id)
            .order_by(LongTermMemory.embedding.cosine_distance(embedding))
            .limit(top_k)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()