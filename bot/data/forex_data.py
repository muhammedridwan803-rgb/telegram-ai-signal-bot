import os
import requests
import pandas as pd
import yfinance as yf

ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")


def _alpha_fx(pair, interval="60min"):
    base = pair[:3]
    quote = pair[3:]

    url = "https://www.alphavantage.co/query"
    params = {
        "function": "FX_INTRADAY",
        "from_symbol": base,
        "to_symbol": quote,
        "interval": interval,
        "apikey": ALPHAVANTAGE_API_KEY,
        "outputsize": "compact",
    }

    r = requests.get(url, params=params, timeout=15)
    data = r.json()

    key = f"Time Series FX ({interval})"
    if key not in data:
        return None

    df = pd.DataFrame.from_dict(data[key], orient="index")
    df = df.rename(columns={
        "1. open": "open",
        "2. high": "high",
        "3. low": "low",
        "4. close": "close",
    })

    df["volume"] = 0
    df = df.astype(float).sort_index()
    return df


def _alpha_commodity(symbol):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "COMMODITY_INTRADAY",
        "symbol": symbol,
        "interval": "60min",
        "apikey": ALPHAVANTAGE_API_KEY,
    }

    r = requests.get(url, params=params, timeout=15)
    data = r.json()

    key = "Time Series (60min)"
    if key not in data:
        return None

    df = pd.DataFrame.from_dict(data[key], orient="index")
    df = df.rename(columns={
        "1. open": "open",
        "2. high": "high",
        "3. low": "low",
        "4. close": "close",
    })

    df["volume"] = 0
    df = df.astype(float).sort_index()
    return df


def get_forex_data(pair, interval="1h"):
    pair = pair.upper()

    # ---- TRY YFINANCE FIRST (NORMAL FOREX) ----
    try:
        symbol = pair + "=X"
        df = yf.download(symbol, period="30d", interval="1h", auto_adjust=False, progress=False)

        if df is not None and not df.empty:
            df = df.rename(columns={
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume",
            })

            df = df[["open", "high", "low", "close", "volume"]]
            price = float(df["close"].squeeze().iloc[-1])

            return {"df": df, "price": price, "source": "yfinance"}

    except Exception:
        pass

    # ---- GOLD / SILVER (COMMODITY) ----
    if pair in ["XAUUSD", "XAGUSD"]:
        df = _alpha_commodity(pair.replace("USD", ""))
        if df is not None:
            return {
                "df": df,
                "price": float(df["close"].iloc[-1]),
                "source": "alphavantage_commodity",
            }

    # ---- FOREX FALLBACK ----
    df = _alpha_fx(pair)
    if df is not None:
        return {
            "df": df,
            "price": float(df["close"].iloc[-1]),
            "source": "alphavantage_fx",
        }

    return None
