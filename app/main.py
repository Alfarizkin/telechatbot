from fastapi import FastAPI
from .telegram_bot import router
from .database import engine
from .models import Base

app = FastAPI()
app.include_router(router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)