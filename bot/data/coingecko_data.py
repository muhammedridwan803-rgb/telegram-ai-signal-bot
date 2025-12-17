import requests

COINGECKO_API = "https://api.coingecko.com/api/v3"

def get_coingecko_price(symbol: str):
    # Expect symbols like BTCUSDT, ETHUSDT
    coin = symbol.replace("USDT", "").lower()

    url = f"{COINGECKO_API}/simple/price"
    params = {
        "ids": coin,
        "vs_currencies": "usd"
    }

    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()

        if coin not in data:
            return None

        return {
            "price": data[coin]["usd"],
            "df": None  # no candles → no indicators
        }
    except Exception:
        return None
