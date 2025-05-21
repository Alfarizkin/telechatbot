from fastapi import FastAPI
from app.telegram_bot import router, application 
from app.database import engine
from app.models import Base

app = FastAPI()
app.include_router(router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Start telegram bot application
    await application.initialize()
    await application.start()
    print("Telegram bot started")