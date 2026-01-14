from sqlalchemy.ext.asyncio import AsyncSession
from ..repositories.chat_log import ChatLogRepository
from ..ai.ai_client import ask_ai
from ..cores.exception import DatabaseError, AIServiceError, ChatServiceError
from typing import List
from app.schemas.chat_history import ChatMessageSchema

class ChatService:
    def __init__(
            self,
            session: AsyncSession
            ):
        self.session = session
        self.repo = ChatLogRepository(session)
        self.ai = ask_ai

    async def handle_chat(
        self,
        chat_id: str,
        ai_name: str,
        ai_identity: str,
        ai_rules: str,
        user_prompt: str,
    ):
        try:
            history = await self.repo.get_recent_message(
                chat_id=chat_id,
                limit = 15
            )

            await self.repo.add_message(
                chat_id=chat_id,
                role="user",
                content=user_prompt
            )
    
            system_prompt = {"role": "system", "content": 
                                f"Roleplay Identity: {ai_identity}\n"
                                f"Behavioral Rules: {ai_rules}\n"
                                f"Current Persona: You are {ai_name}. Stay in character."}
    
            messages = [system_prompt]
            messages += [
                {"role": h.role, "content": h.content}
                for h in history
            ]
            messages.append({"role": "user", "content": user_prompt})

            try:
                ai_reply = await self.ai(messages)
            except Exception as e:
                raise AIServiceError(f"AI Request Failed: {e}")

            await self.repo.add_message(
                chat_id=chat_id,
                role="assistant",
                content=ai_reply
            )

            try:
                await self.session.commit()
            except Exception as e:
                raise DatabaseError(f"Error Commit Database: {e}")

            return ai_reply
        except Exception:
            await self.session.rollback()
            raise

    async def get_history_chat(
        self,
        chat_id: str,
    ) -> List[ChatMessageSchema]:
        try:
            history = await self.repo.get_all_message(chat_id)
            messages =[ChatMessageSchema.model_validate(h) for h in history]
            return messages
        except DatabaseError:
            raise
        except Exception as e:
            raise ChatServiceError(f"Error getting history: {e}")