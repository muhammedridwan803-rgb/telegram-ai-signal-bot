from telegram import Update
from telegram.ext import ContextTypes

async def image_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Analyzing chart visually…"

    # SAFE reply handling
    if update.message:
        await update.message.reply_text(text)
    elif update.callback_query and update.callback_query.message:
        await update.callback_query.message.reply_text(text)

    # 👉 your image analysis logic continues below
    # (keep existing code if any)
