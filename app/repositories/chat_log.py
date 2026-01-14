from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from ..models.chat_log import ChatLog

class ChatLogRepository:
    def __init__(
            self,
            session: AsyncSession
            ):
        self.session = session

    async def add_message(
        self,
        chat_id: str,
        role: str,
        content: str
    ):
        msg = ChatLog(
            chat_id=chat_id,
            role=role,
            content=content
        )
        self.session.add(msg)
        return msg
    
    async def get_recent_message(
        self,
        chat_id: str,
        limit: int = 10
    ):
        stmt = (
            select(ChatLog)
            .where(ChatLog.chat_id == chat_id)
            .order_by(ChatLog.created_at.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(reversed(result.scalars().all()))
   
    async def get_all_message(
        self,
        chat_id: str
    ) -> List["ChatLog"]:
        stmt = (
            select(ChatLog)
            .where(ChatLog.chat_id == chat_id)
            .order_by(ChatLog.created_at.asc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()