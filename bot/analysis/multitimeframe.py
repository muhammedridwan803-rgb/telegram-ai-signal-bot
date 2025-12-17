from bot.data.market_router import get_market_data

def multi_tf_context(pair: str):
    data = get_market_data(pair)

    if not data or not data.get("df"):
        return "Multi-timeframe data unavailable."

    df = data["df"]

    try:
        trend = "Bullish" if df["Close"].iloc[-1] > df["Close"].mean() else "Bearish"
        return f"Higher timeframe bias: {trend}"
    except Exception:
        return "Multi-timeframe analysis failed."
