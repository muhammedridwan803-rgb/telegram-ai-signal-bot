def detect_conflicts(indicators, setup):
    conflicts = []

    trend = indicators.get("trend")
    macd = indicators.get("macd")
    rsi_state = indicators.get("rsi_state")
    volume = indicators.get("volume")
    structure = setup.get("structure")

    # ---- Trend vs Momentum ----
    if trend == "Bullish" and macd == "Bearish":
        conflicts.append("Trend is bullish, but MACD shows bearish momentum.")
    elif trend == "Bearish" and macd == "Bullish":
        conflicts.append("Trend is bearish, but MACD shows bullish counter-momentum.")

    # ---- Structure vs EMA Trend ----
    if structure and trend and structure != trend:
        conflicts.append("Market structure and EMA trend are not aligned.")

    # ---- RSI Risk ----
    if rsi_state == "Overbought" and trend == "Bullish":
        conflicts.append("RSI is overbought, increasing pullback risk.")
    elif rsi_state == "Oversold" and trend == "Bearish":
        conflicts.append("RSI is oversold, increasing bounce risk.")

    # ---- Volume Warning ----
    if volume == "Low":
        conflicts.append("Low volume environment reduces setup reliability.")

    return conflicts
