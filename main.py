from fastapi import FastAPI
from app.cores.database import engine, Base

from app.routers.chat_api import router_chat
from app.routers.long_term_memory import router_memory
from app.routers.index import router_index
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Chat API for Unity")

async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router_index, tags=["Landing"])
app.include_router(router_chat)
app.include_router(router_memory)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)