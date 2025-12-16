import pandas as pd


def detect_zones(df, lookback=50):
    if df is None or len(df) < lookback:
        return []

    zones = []
    recent = df.tail(lookback)

    for i in range(2, len(recent) - 2):
        candle = recent.iloc[i]
        prev = recent.iloc[i - 1]

        # ---- FORCE SCALARS ----
        open_ = float(candle["open"].iloc[0] if isinstance(candle["open"], pd.Series) else candle["open"])
        close_ = float(candle["close"].iloc[0] if isinstance(candle["close"], pd.Series) else candle["close"])
        high_ = float(candle["high"].iloc[0] if isinstance(candle["high"], pd.Series) else candle["high"])
        low_ = float(candle["low"].iloc[0] if isinstance(candle["low"], pd.Series) else candle["low"])

        prev_open = float(prev["open"].iloc[0] if isinstance(prev["open"], pd.Series) else prev["open"])
        prev_close = float(prev["close"].iloc[0] if isinstance(prev["close"], pd.Series) else prev["close"])

        body = abs(close_ - open_)
        rng = abs(high_ - low_)

        if body == 0:
            continue

        # ---- IMPULSE CANDLE ----
        if rng > body * 2:
            base_high = max(prev_open, prev_close)
            base_low = min(prev_open, prev_close)

            zones.append(
                {
                    "type": "Demand" if close_ > open_ else "Supply",
                    "high": base_high,
                    "low": base_low,
                    "freshness": "Fresh",
                    "departure": "Strong",
                }
            )

    return zones[:3]
