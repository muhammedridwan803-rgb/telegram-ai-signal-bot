from telegram import Update
from telegram.ext import ContextTypes


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🤖 *Call Hunter v2 — Help Guide*\n\n"
        "Advanced market analysis using live data, indicators, AI reasoning, "
        "and visual chart analysis.\n"
        "_Educational only — NOT a signal bot._\n\n"

        "━━━━━━━━━━━━━━\n"
        "📌 *AVAILABLE COMMANDS*\n"
        "━━━━━━━━━━━━━━\n\n"

        "💎 */price PAIR*\n"
        "Live market snapshot:\n"
        "• Price\n"
        "• Trend & EMA structure\n"
        "• RSI, MACD, Volume\n"
        "• AI market insight\n\n"
        "_Example:_ `/price BTCUSDT`\n\n"

        "🧠 */setup PAIR*\n"
        "Advanced market framework:\n"
        "• HTF / LTF bias\n"
        "• Premium / Discount\n"
        "• Demand & Supply zones\n"
        "• POIs, risk & confidence\n"
        "• Trade framework ideas (no entries)\n\n"
        "_Example:_ `/setup XAUUSD`\n\n"

        "📸 *Chart Screenshot Analysis*\n"
        "Send a chart screenshot.\n"
        "• Add *analyze* as caption, OR\n"
        "• Reply with `/analyze`\n\n"
        "The bot will analyze:\n"
        "• Trend & structure\n"
        "• POIs & interest zones\n"
        "• BOS / CHOCH (if visible)\n"
        "• Bias & confidence score\n\n"

        "🧠 */analyze*\n"
        "Used after sending a chart image.\n"
        "Combines visual + live data + MTF.\n\n"

        "━━━━━━━━━━━━━━\n"
        "⚠️ *IMPORTANT*\n"
        "━━━━━━━━━━━━━━\n"
        "• No buy/sell signals\n"
        "• No financial advice\n"
        "• Analysis only\n"
        "• Always wait for confirmation\n\n"

        "━━━━━━━━━━━━━━\n"
        "📞 *SUPPORT & CUSTOM BOTS*\n"
        "━━━━━━━━━━━━━━\n"
        "🐦 X (Twitter): https://x.com/Shiller_xx\n"
        "📲 Telegram: https://t.me/Shiller_xxx\n\n"
        "Stay disciplined 🧘‍♂️📊"
    )

    await update.message.reply_text(text, parse_mode="Markdown")
