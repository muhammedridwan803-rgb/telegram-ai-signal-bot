import pandas as pd


def assess_risk(df, zones, indicators):
    if df is None or df.empty or not zones:
        return {
            "risk_label": "Unknown",
            "risk_text": "Risk cannot be assessed due to limited data.",
        }

    z = zones[0]

    # ---- FORCE FLOATS ----
    zone_high = float(z.get("high"))
    zone_low = float(z.get("low"))
    zone_size = abs(zone_high - zone_low)

    recent = df.tail(20)

    highs = recent["high"].squeeze()
    lows = recent["low"].squeeze()

    if not isinstance(highs, pd.Series):
        highs = pd.Series(highs)
    if not isinstance(lows, pd.Series):
        lows = pd.Series(lows)

    ranges = (highs - lows).astype(float)
    avg_range = float(ranges.mean())

    # ---- RISK LOGIC ----
    if zone_size < avg_range * 0.8:
        risk = "Tight"
    elif zone_size < avg_range * 1.6:
        risk = "Moderate"
    else:
        risk = "Wide"

    explanation = {
        "Tight": "Zone is compact relative to recent volatility.",
        "Moderate": "Zone size aligns with recent market volatility.",
        "Wide": "Zone is large compared to volatility, increasing risk.",
    }

    return {
        "risk_label": risk,
        "risk_text": explanation.get(risk),
    }
