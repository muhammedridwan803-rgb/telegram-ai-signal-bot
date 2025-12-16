from bot.data.crypto_data import get_crypto_data
from bot.data.forex_data import get_forex_data


def get_market_data(pair, interval="1h"):
    pair = pair.upper()

    # Simple forex detection (EURUSD, GBPJPY, etc.)
    if len(pair) == 6 and pair.isalpha():
        return get_forex_data(pair, interval)

    # Default to crypto
    return get_crypto_data(pair, interval)
