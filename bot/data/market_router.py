from bot.data.yahoo_data import get_yahoo_data
from bot.data.coingecko_data import get_coingecko_price

def get_market_data(pair: str):
    # 1️⃣ Try Yahoo (full OHLC → indicators)
    data = get_yahoo_data(pair)
    if data:
        return data

    # 2️⃣ Fallback: CoinGecko (price only)
    return get_coingecko_price(pair)
