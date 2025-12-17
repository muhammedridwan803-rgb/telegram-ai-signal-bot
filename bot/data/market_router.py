import yfinance as yf

def get_market_data(pair: str):
    try:
        ticker = yf.Ticker(pair)
        data = ticker.history(period="1d", interval="5m")

        if data.empty:
            return None

        price = round(float(data["Close"].iloc[-1]), 5)
        return {
            "price": price,
            "df": data
        }

    except Exception:
        return None
