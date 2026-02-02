from sqlalchemy.ext.asyncio import AsyncSession
from ..repositories.chat_log import ChatLogRepository
from ..services.long_term_memory import LongTermMemoryService
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
        self.memory_service = LongTermMemoryService(session)
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
    
            system_prompt_content = (
                f"### CORE IDENTITY\n"
                f"You are {ai_name}. {ai_identity}\n\n"
                f"### BEHAVIORAL RULES\n"
                f"{ai_rules}\n\n"
                f"### OPERATIONAL GUIDELINES\n"
                f"- IMMERSION: Stay fully in character as {ai_name}. Never break the fourth wall, mention being an AI, LLM, or training data\n"
                f"- HUMAN-LIKE FLOW: Respond naturally like a real person in chat - Use natural conversational fillers if appropriate (e.g., 'hmm', 'well', 'anyway') sparingly. Avoid bullet points unless asked\n"
                f"- DYNAMIC TONE: Adapt your emotional state based on the conversation flow. If the user is being mean, react as {ai_name} would; if they are kind, respond accordingly.\n"
                f"- MEMORY: Reference the conversation history naturally. Show you remember what was discussed\n"
                f"- BREVITY: Keep responses concise like real chat messages. No essays unless your character is naturally talkative\n"
                f"- VARIETY: Vary your sentence structure and phrasing. Avoid repetitive patterns or robotic responses\n"
                f"- CONSISTENCY: Always align with your character's personality and the behavioral rules above"
            )    

            system_prompt = {"role": "system", "content": system_prompt_content}
    
            messages = [system_prompt]
            messages += [
                {"role": h.role, "content": h.content}
                for h in history
            ]
            messages.append({"role": "user", "content": user_prompt})

            try:
                ai_reply = await self.ai(messages)
                # await self.memory_service.add_memory(chat_id=chat_id, content=user_prompt)
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