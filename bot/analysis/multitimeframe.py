from bot.data.crypto_data import get_crypto_data
from bot.analysis.indicators import analyze_indicators
from bot.analysis.structure import detect_structure

def analyze_timeframe(symbol, interval):
    data = get_crypto_data(symbol, interval=interval)
    if not data or data.get("df") is None:
        return {}

    df = data["df"]
    ind = analyze_indicators(df)
    struct = detect_structure(df)

    return {
        "trend": ind.get("trend"),
        "structure": struct.get("structure")
    }


def multi_tf_context(symbol):
    htf = analyze_timeframe(symbol, "4h")
    ltf = analyze_timeframe(symbol, "1h")

    return {
        "HTF": htf,  # Higher timeframe
        "LTF": ltf   # Lower timeframe
    }
