from telegram import Update
from telegram.ext import ContextTypes

from bot.state import LAST_IMAGE
from bot.analysis.vision import analyze_chart_image


async def image_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    photo = update.message.photo[-1]

    LAST_IMAGE[user_id] = {
        "file_id": photo.file_id,
        "chat_id": update.effective_chat.id,
    }

    # Optional acknowledgement
    if update.message.caption and "analyze" in update.message.caption.lower():
        await update.message.reply_text("🧠 Analyzing chart visually…")

        file = await context.bot.get_file(photo.file_id)
        image_bytes = await file.download_as_bytearray()

        # SAFE EMPTY CONTEXT (visual-only)
        ai_text = analyze_chart_image(
            bytes(image_bytes),
            context={}
        )

        await update.message.reply_text(ai_text)
