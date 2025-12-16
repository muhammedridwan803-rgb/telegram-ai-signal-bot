import pandas as pd


def detect_structure(df, lookback=20):
    if df is None or len(df) < lookback:
        return {}

    recent = df.tail(lookback)

    highs = recent["high"].squeeze()
    lows = recent["low"].squeeze()

    if not isinstance(highs, pd.Series):
        highs = pd.Series(highs)
    if not isinstance(lows, pd.Series):
        lows = pd.Series(lows)

    recent_highs = highs.tail(2).values
    recent_lows = lows.tail(2).values

    higher_highs = recent_highs[-1] > recent_highs[0]
    higher_lows = recent_lows[-1] > recent_lows[0]

    lower_highs = recent_highs[-1] < recent_highs[0]
    lower_lows = recent_lows[-1] < recent_lows[0]

    if higher_highs and higher_lows:
        structure = "Bullish"
    elif lower_highs and lower_lows:
        structure = "Bearish"
    else:
        structure = "Range"

    return {
        "structure": structure,
        "swing_high": float(highs.max()),
        "swing_low": float(lows.min()),
    }
