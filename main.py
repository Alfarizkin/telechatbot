from fastapi import FastAPI
from app.chat_api import router

app = FastAPI(title="Chat API for Unity")

app.include_router(router)
