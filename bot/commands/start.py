from telegram import Update
from telegram.ext import ContextTypes


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 Welcome to *Call Hunter v2*\n\n"
        "This bot helps you *analyze markets like a trader*, not chase signals.\n\n"

        "🧠 What it does:\n"
        "• Live crypto & forex analysis\n"
        "• Institutional-style market context\n"
        "• AI reasoning (not random text)\n"
        "• Chart screenshot analysis\n\n"

        "🚫 What it does NOT do:\n"
        "• No buy/sell signals\n"
        "• No guaranteed profits\n\n"

        "▶️ Get started:\n"
        "• `/price BTCUSDT`\n"
        "• `/setup XAUUSD`\n"
        "• Send a chart image + type *analyze*\n\n"

        "📖 Use `/help` to see all features.\n\n"
        "Trade smart. Protect capital. 📊🧘‍♂️"
    )

    await update.message.reply_text(text, parse_mode="Markdown")
