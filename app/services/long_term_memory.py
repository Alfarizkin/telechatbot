from sqlalchemy.ext.asyncio import AsyncSession
from ..repositories.long_term_memory import LongTermMemoryRepository
from ..cores.exception import DatabaseError, AIServiceError, ChatServiceError
from ..ai.ai_client import ask_ai
import json
from typing import List, TypedDict, Union
from app.schemas.long_term_memory import LongTermMemorySchema, AddMemoryResponse
from sentence_transformers import SentenceTransformer

MODEL = SentenceTransformer('all-MiniLM-L6-v2')

class AIReply(TypedDict):
    is_important: bool
    reason: str

class LongTermMemoryService:
    def __init__(
            self,
            session: AsyncSession
            ):
        self.session = session
        self.repo = LongTermMemoryRepository(session)
        self.ai = ask_ai
        self.model = MODEL
    async def add_memory(
        self,
        chat_id: str,
        content: str,
    ) -> Union[LongTermMemorySchema, dict]:
        system_content = """
            Kamu adalah Memory Manager AI. Tugasmu menentukan apakah sebuah pesan dari user layak disimpan dalam Long Term Memory.

            Kriteria Memori LAYAK SIMPAN (True):
            - Berisi informasi personal user (nama, hobi, pekerjaan, preferensi).
            - Berisi fakta penting yang mungkin ditanyakan lagi nanti.
            - Berisi instruksi khusus tentang cara AI harus berperilaku.

            Kriteria Memori TIDAK LAYAK SIMPAN (False):
            - Hanya sapaan (Halo, Pagi, dll).
            - Pertanyaan umum yang tidak bersifat personal (Apa itu Bumi?).
            - Pesan singkat tanpa konteks (Ok, Siap, Cek).
            - Typo atau pesan yang tidak jelas maksudnya.

            OUTPUT:
            Berikan jawaban HANYA dalam format JSON: {"is_important": boolean, "reason": "alasan singkat"}
            """

            # Komponen Message List
        messages = [
                {"role": "system", "content": system_content},
                {"role": "user", "content": f"Evaluasi pesan ini: '{content}'"}
            ]

        try:
            ai_reply = await self.ai(messages)
            try:
                result_json: AIReply = json.loads(ai_reply)
            except json.JSONDecodeError:
                result_json = {"is_important": False, "reason": "Invalid AI response"}
        except Exception as e:
            raise AIServiceError(f"AI Request Failed: {e}")
        
        if not result_json.get("is_important", False):
            return {"saved": False, "reason": result_json.get("reason", "Not important")}
        
        try:
            embedding = self.model.encode(content).tolist()
            memory = await self.repo.add_memory(
                chat_id=chat_id,
                content=content,
                embedding=embedding
            )

            return AddMemoryResponse(saved=True, memory=LongTermMemorySchema.model_validate(memory))
        except Exception as e:
            raise DatabaseError(f"Failed to add memory: {str(e)}")
        
    async def search_memory(
        self,
        chat_id: str,
        query: str,
        top_k: int = 5
    ) -> List[LongTermMemorySchema]:
        query_embedding = self.model.encode(query).tolist()

        memories = await self.repo.search_similar_memory(
            chat_id=chat_id,
            embedding=query_embedding,
            top_k=top_k
        )

        return [LongTermMemorySchema.model_validate(m) for m in memories]