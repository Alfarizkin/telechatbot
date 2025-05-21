from fastapi import APIRouter, Request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler
from telegram.ext import ContextTypes
from .config import TELEGRAM_TOKEN
from .ai_client import ask_ai
from .models import Message
from .database import SessionLocal

router = APIRouter()
bot = Bot(token=TELEGRAM_TOKEN)
application = Application.builder().token(TELEGRAM_TOKEN).build()

@router.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, bot)
    await application.update_queue.put(update)
    return {"ok": True}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = "Halo!"
    ai_response = await ask_ai(user_input)

    await update.message.reply_text(ai_response)

    # Simpan ke database
    async with SessionLocal() as session:
        msg = Message(
            user_id=str(update.effective_user.id),
            message=user_input,
            reply=ai_response
        )
        session.add(msg)
        await session.commit()

application.add_handler(CommandHandler("start", start))