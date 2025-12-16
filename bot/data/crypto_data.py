import pandas as pd
import requests
from binance.client import Client
from binance.exceptions import BinanceAPIException

client = Client()

def get_binance_klines(symbol, interval="1h", limit=200):
    try:
        klines = client.get_klines(
            symbol=symbol.upper(),
            interval=interval,
            limit=limit
        )

        df = pd.DataFrame(klines, columns=[
            "open_time","open","high","low","close","volume",
            "close_time","quote_volume","trades",
            "taker_buy_base","taker_buy_quote","ignore"
        ])

        df = df[["open_time","open","high","low","close","volume"]]
        df = df.astype(float)
        return df

    except BinanceAPIException:
        return None
    except Exception:
        return None


def get_coingecko_price(symbol):
    try:
        base = symbol.replace("USDT", "").lower()
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": base,
            "vs_currencies": "usd"
        }
        r = requests.get(url, params=params, timeout=10)
        return r.json().get(base, {}).get("usd")
    except Exception:
        return None


def get_crypto_data(symbol, interval="1h"):
    df = get_binance_klines(symbol, interval)

    if df is not None and len(df) >= 50:
        return {
            "source": "binance",
            "df": df,
            "price": float(df["close"].iloc[-1])
        }

    price = get_coingecko_price(symbol)
    if price:
        return {
            "source": "coingecko",
            "df": None,
            "price": price
        }

    return None
