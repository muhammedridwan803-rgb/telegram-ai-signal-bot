from telegram import Update
from telegram.ext import ContextTypes

from bot.state import LAST_IMAGE
from bot.data.market_router import get_market_data
from bot.analysis.indicators import analyze_indicators
from bot.analysis.multitimeframe import multi_tf_context
from bot.analysis.session import get_market_session
from bot.analysis.vision import analyze_chart_image


async def analyze_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in LAST_IMAGE:
        await update.message.reply_text("❌ Send a chart image first.")
        return

    data = LAST_IMAGE[user_id]
    file = await context.bot.get_file(data["file_id"])
    image_bytes = await file.download_as_bytearray()

    # Try to infer pair from caption (optional)
    pair = None
    if update.message.reply_to_message and update.message.reply_to_message.text:
        pair = update.message.reply_to_message.text.strip().upper()

    market = get_market_data(pair) if pair else None
    indicators = analyze_indicators(market["df"]) if market else {}
    tf = multi_tf_context(pair) if pair else {}
    session = get_market_session()

    context_payload = {
        "price": market.get("price") if market else "Unknown",
        "htf": tf.get("HTF", {}).get("structure"),
        "ltf": tf.get("LTF", {}).get("structure"),
        "ema": indicators.get("ema_state"),
        "rsi": indicators.get("rsi"),
        "rsi_state": indicators.get("rsi_state"),
        "session": session.get("session"),
    }

    await update.message.reply_text("🧠 Analyzing chart with data & structure…")

    ai_text = analyze_chart_image(bytes(image_bytes), context_payload)

    await update.message.reply_text(ai_text)
