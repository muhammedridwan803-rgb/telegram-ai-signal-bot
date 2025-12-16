from bot.analysis.llm_client import llm_explain


def _fallback_explanation(a):
    trend = a.get("trend")
    macd = a.get("macd")
    rsi = a.get("rsi")
    rsi_state = a.get("rsi_state")
    volume = a.get("volume")

    lines = []

    if trend == "Bearish":
        lines.append("Sellers are dominating the broader market structure.")
    elif trend == "Bullish":
        lines.append("Buyers are controlling the broader market structure.")
    else:
        lines.append("Market structure is neutral with no clear dominance.")

    if macd == "Bullish" and trend == "Bearish":
        lines.append("Short-term bullish momentum is forming against the dominant bearish trend.")
    elif macd == "Bearish" and trend == "Bullish":
        lines.append("Short-term bearish momentum is appearing within a broader bullish trend.")
    elif macd == "Bullish":
        lines.append("Momentum supports further upside.")
    elif macd == "Bearish":
        lines.append("Momentum supports further downside.")
    else:
        lines.append("Momentum lacks confirmation.")

    lines.append(f"RSI at {rsi} remains {rsi_state.lower()}.")
    lines.append(f"Volume is {volume.lower()}, affecting conviction.")

    lines.append("Overall conditions are mixed; confirmation is advised.")
    return " ".join(lines)


def generate_ai_analysis(analysis):
    if not analysis:
        return "Insufficient market data for analysis."

    prompt = f"""
Market snapshot:
- Trend (EMA): {analysis.get('trend')}
- EMA State: {analysis.get('ema_state')}
- RSI: {analysis.get('rsi')} ({analysis.get('rsi_state')})
- MACD: {analysis.get('macd')}
- Volume: {analysis.get('volume')}

Explain this clearly to a trader.
Handle conflicts between trend and momentum.
No hype. No signals. Analysis only.
"""

    llm_text = llm_explain(prompt)
    return llm_text if llm_text else _fallback_explanation(analysis)
