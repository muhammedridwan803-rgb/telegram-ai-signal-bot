from telegram import Update
from telegram.ext import ContextTypes

from bot.data.market_router import get_market_data
from bot.analysis.indicators import analyze_indicators
from bot.analysis.setup_engine import evaluate_setup
from bot.analysis.multitimeframe import multi_tf_context
from bot.analysis.llm_client import llm_explain
from bot.analysis.risk import assess_risk
from bot.analysis.conflicts import detect_conflicts
from bot.analysis.session import get_market_session
from bot.utils.helpers import (
    emoji_trend,
    emoji_level,
    emoji_status,
    emoji_location,
    emoji_zone,
    emoji_departure,
    emoji_risk,
    emoji_conflict,
    emoji_session,
    emoji_volatility,
)


async def setup_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Usage: /setup PAIR\nExamples: /setup BTCUSDT | /setup EURUSD"
        )
        return

    pair = context.args[0].upper()
    data = get_market_data(pair)

    if not data or data.get("df") is None:
        await update.message.reply_text("❌ Setup analysis unavailable for this pair.")
        return

    df = data["df"]
    indicators = analyze_indicators(df)
    setup = evaluate_setup(df, indicators)
    tf = multi_tf_context(pair)
    risk = assess_risk(df, setup.get("zones"), indicators)
    conflicts = detect_conflicts(indicators, setup)
    session = get_market_session()

    if not setup:
        await update.message.reply_text("⚠️ Not enough data to build a setup.")
        return

    price = setup.get("current_price")

    # ================= SUMMARY CARD =================
    msg = []
    msg.append("🧾 Setup Summary")
    msg.append(f"💎 {pair}")
    msg.append(f"🏷 Price: {price}")

    msg.append(
        f"⏱ HTF (4H): {emoji_trend(tf.get('HTF', {}).get('structure'))} "
        f"{tf.get('HTF', {}).get('structure')}"
    )
    msg.append(
        f"⏱ LTF (1H): {emoji_trend(tf.get('LTF', {}).get('structure'))} "
        f"{tf.get('LTF', {}).get('structure')}"
    )

    msg.append(
        f"🌍 Session: {emoji_session(session.get('session'))} "
        f"{session.get('session')} "
        f"({emoji_volatility(session.get('volatility'))} {session.get('volatility')})"
    )

    msg.append(
        f"📍 Location: {emoji_location(setup.get('price_location'))} "
        f"{setup.get('price_location')}"
    )
    msg.append(
        f"⭐ Quality: {emoji_level(setup.get('quality_label'))} "
        f"{setup.get('quality_label')} ({setup.get('quality_score')}/100)"
    )
    msg.append(
        f"🔐 Confidence: {emoji_level(setup.get('confidence_label'))} "
        f"{setup.get('confidence_label')} ({setup.get('confidence_score')}%)"
    )
    msg.append(
        f"🚦 Status: {emoji_status(setup.get('status'))} {setup.get('status')}"
    )
    msg.append(
        f"⚖️ Risk: {emoji_risk(risk.get('risk_label'))} {risk.get('risk_label')}"
    )
    msg.append("")

    # ================= CONFLICTS =================
    if conflicts:
        msg.append("⚠️ Conflicts Detected")
        for c in conflicts:
            msg.append(f"{emoji_conflict()} {c}")
        msg.append("")

    # ================= ZONE DETAILS =================
    if setup.get("zones"):
        z = setup["zones"][0]
        msg.append("🧱 Zone Details")
        msg.append(
            f"• {z.get('type')} Zone: "
            f"{emoji_zone(z.get('freshness'))} {z.get('freshness')} | "
            f"{emoji_departure(z.get('departure'))} {z.get('departure')} departure"
        )
        msg.append("")

    # ================= TRADE FRAMEWORK =================
    if setup.get("framework"):
        fw = setup["framework"]
        msg.append("📘 Trade Framework (Ideas)")
        msg.append(f"• Bias: {fw.get('bias')}")
        msg.append(f"• Entry Zone: {fw.get('entry_zone')}")
        msg.append(f"• Invalidation: {fw.get('invalidation')}")
        msg.append(f"• Target Area: {fw.get('target')}")
        msg.append("")

    # ================= AI REASONING =================
    prompt = f"""
You are a professional market analyst.

Summary:
- Pair: {pair}
- Price: {price}
- Session: {session.get('session')} ({session.get('volatility')})
- HTF structure: {tf.get('HTF', {}).get('structure')}
- LTF structure: {tf.get('LTF', {}).get('structure')}
- Location: {setup.get('price_location')}
- Quality: {setup.get('quality_label')}
- Confidence: {setup.get('confidence_label')}
- Status: {setup.get('status')}
- Risk: {risk.get('risk_label')}
- Conflicts: {conflicts}

Indicators:
- EMA Trend: {indicators.get('trend')}
- RSI: {indicators.get('rsi')} ({indicators.get('rsi_state')})
- MACD: {indicators.get('macd')}
- Volume: {indicators.get('volume')}

Zones:
{setup.get('zones')}

Explain clearly. Educational only. No signals.
"""

    ai_text = llm_explain(prompt) or "👀 Area to watch. Wait for confirmation."

    msg.append("🧠 AI Reasoning")
    msg.append(ai_text)
    msg.append("")
    msg.append("🛑 Not a signal. 🧘 Patience pays.")

    await update.message.reply_text("\n".join(msg))
