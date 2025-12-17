import yfinance as yf
from bot.data.coingecko_data import get_crypto_price

def get_market_data(pair: str):
    # 1️⃣ Try yfinance first
    try:
        ticker = yf.Ticker(pair)
        data = ticker.history(period="1d", interval="5m")

        if not data.empty:
            price = round(float(data["Close"].iloc[-1]), 5)
            return {
                "price": price,
                "df": data
            }
    except Exception:
        pass

    # 2️⃣ Fallback to CoinGecko (crypto only)
    return get_crypto_price(pair)
