from telegram import Update
from telegram.ext import ContextTypes

from bot.data.market_router import get_market_data
from bot.analysis.indicators import analyze_indicators
from bot.analysis.ai_analysis import generate_ai_analysis


async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /price PAIR\nExamples: /price BTCUSDT | /price EURUSD")
        return

    pair = context.args[0].upper()
    data = get_market_data(pair)

    if not data:
        await update.message.reply_text("❌ Price not available for this pair.")
        return

    price = data.get("price")
    df = data.get("df")

    analysis = analyze_indicators(df) if df is not None else {}
    ai_text = generate_ai_analysis(analysis)

    msg = []
    msg.append(f"💎 Pair: {pair}")
    msg.append(f"🏷 Price: {price}")
    msg.append("")
    msg.append("📊 Market Analysis")

    if analysis:
        msg.append(f"📈 Trend: {analysis.get('trend')}")
        msg.append(f"📉 EMA: {analysis.get('ema_state')}")
        msg.append(f"📊 RSI: {analysis.get('rsi')} ({analysis.get('rsi_state')})")
        msg.append(f"📈 MACD: {analysis.get('macd')}")
        msg.append(f"📦 Volume: {analysis.get('volume')}")
    else:
        msg.append("⚠️ Indicator data unavailable.")

    msg.append("")
    msg.append("🧠 AI Analysis")
    msg.append(ai_text)
    msg.append("")
    msg.append("🛑 Not a signal.")

    await update.message.reply_text("\n".join(msg))
