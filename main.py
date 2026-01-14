from fastapi import FastAPI
from app.cores.database import engine, Base

from app.routers.chat_api import router
from app.routers.index import router_index
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Chat API for Unity")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(router_index, tags=["Landing"])
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)