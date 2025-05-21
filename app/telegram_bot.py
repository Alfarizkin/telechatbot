from fastapi import APIRouter, Request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from .config import TELEGRAM_TOKEN
from .ai_client import ask_ai
from .models import Message
from .database import SessionLocal

router = APIRouter()

# Buat aplikasi Telegram
application = Application.builder().token(TELEGRAM_TOKEN).build()

# Endpoint webhook
@router.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, application.bot)
    await application.update_queue.put(update)
    return {"ok": True}

# Handler untuk /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hai! Kirim pesan apa pun untuk mulai ngobrol dengan AI.")

# Handler untuk semua pesan teks
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
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

# Tambahkan handler ke aplikasi
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
