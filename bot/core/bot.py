from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
)

from bot.commands.start import start_command
from bot.commands.help import help_command
from bot.commands.price import price_command
from bot.commands.setup import setup_command
from bot.commands.analyze import analyze_command
from bot.handlers.image import image_handler


def build_app(token: str):
    app = ApplicationBuilder().token(token).build()

    # ─── BASIC COMMANDS ─────────────────────────────
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))

    # ─── MARKET COMMANDS ────────────────────────────
    app.add_handler(CommandHandler("price", price_command))
    app.add_handler(CommandHandler("setup", setup_command))
    app.add_handler(CommandHandler("analyze", analyze_command))

    # ─── IMAGE HANDLER (CHART SCREENSHOTS) ──────────
    app.add_handler(MessageHandler(filters.PHOTO, image_handler))

    return app
