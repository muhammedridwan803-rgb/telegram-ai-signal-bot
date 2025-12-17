import yfinance as yf

def get_yahoo_data(pair: str):
    try:
        ticker = yf.Ticker(pair)
        hist = ticker.history(period="1d", interval="5m")

        if hist.empty:
            return None

        price = float(hist["Close"].iloc[-1])

        return {
            "price": price,
            "df": hist
        }
    except Exception:
        return None
