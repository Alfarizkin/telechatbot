from fastapi import FastAPI
from app.chat_api import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Chat API for Unity")

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)