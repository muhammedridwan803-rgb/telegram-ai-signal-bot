from datetime import datetime, timezone

def get_market_session():
    now = datetime.now(timezone.utc)
    hour = now.hour

    # UTC-based sessions
    if 0 <= hour < 7:
        return {
            "session": "Asia",
            "volatility": "Low–Moderate"
        }
    elif 7 <= hour < 13:
        return {
            "session": "London",
            "volatility": "High"
        }
    elif 13 <= hour < 21:
        return {
            "session": "New York",
            "volatility": "High"
        }
    else:
        return {
            "session": "Overlap / Late NY",
            "volatility": "Moderate"
        }
