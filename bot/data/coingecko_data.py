import requests

COINGECKO_API = "https://api.coingecko.com/api/v3/simple/price"

def get_crypto_price(symbol: str):
    try:
        symbol = symbol.lower().replace("usdt", "").replace("usd", "")
        params = {
            "ids": symbol,
            "vs_currencies": "usd"
        }
        r = requests.get(COINGECKO_API, params=params, timeout=10)
        if r.status_code != 200:
            return None

        data = r.json()
        if symbol not in data:
            return None

        return {
            "price": data[symbol]["usd"],
            "df": None
        }

    except Exception:
        return None
