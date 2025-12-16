import pandas as pd
import ta


def analyze_indicators(df: pd.DataFrame) -> dict:
    if df is None or len(df) < 50:
        return {}

    # ---- FORCE 1D SERIES (IMPORTANT FIX) ----
    close = df["close"].squeeze()
    volume = df["volume"].squeeze()

    if not isinstance(close, pd.Series):
        close = pd.Series(close)
    if not isinstance(volume, pd.Series):
        volume = pd.Series(volume)

    # ---- EMA ----
    ema50_series = ta.trend.EMAIndicator(close, window=50).ema_indicator()
    ema200_series = ta.trend.EMAIndicator(close, window=200).ema_indicator()

    ema50 = float(ema50_series.iloc[-1])
    ema200 = float(ema200_series.iloc[-1])

    if ema50 > ema200:
        trend = "Bullish"
        ema_state = "EMA50 > EMA200"
    elif ema50 < ema200:
        trend = "Bearish"
        ema_state = "EMA50 < EMA200"
    else:
        trend = "Sideways"
        ema_state = "EMA50 ≈ EMA200"

    # ---- RSI ----
    rsi_series = ta.momentum.RSIIndicator(close, window=14).rsi()
    rsi = float(rsi_series.iloc[-1])

    if rsi > 70:
        rsi_state = "Overbought"
    elif rsi < 30:
        rsi_state = "Oversold"
    else:
        rsi_state = "Neutral"

    # ---- MACD ----
    macd_obj = ta.trend.MACD(close)
    macd_hist = float(macd_obj.macd_diff().iloc[-1])

    if macd_hist > 0:
        macd_state = "Bullish"
    elif macd_hist < 0:
        macd_state = "Bearish"
    else:
        macd_state = "Neutral"

    # ---- VOLUME ----
    avg_volume = float(volume.rolling(20).mean().iloc[-1])
    current_volume = float(volume.iloc[-1])

    if current_volume > avg_volume:
        volume_state = "High"
    elif current_volume < avg_volume:
        volume_state = "Low"
    else:
        volume_state = "Normal"

    return {
        "trend": trend,
        "ema_state": ema_state,
        "ema50": ema50,
        "ema200": ema200,
        "rsi": round(rsi, 2),
        "rsi_state": rsi_state,
        "macd": macd_state,
        "volume": volume_state,
    }
