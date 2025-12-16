def emoji_trend(t):
    return "📈" if t == "Bullish" else "📉" if t == "Bearish" else "🔄"

def emoji_level(l):
    return "🟢" if l == "High" else "🟡" if l == "Moderate" else "🔴"

def emoji_status(s):
    return "🟢" if s == "Active" else "🟡" if s == "Forming" else "🔴"

def emoji_location(loc):
    return "🟢" if loc == "Discount" else "🔴" if loc == "Premium" else "⚪"

def emoji_zone(z):
    if z == "Fresh":
        return "🧪"
    if z == "Tested":
        return "♻️"
    return "⚠️"

def emoji_departure(d):
    return "💥" if d == "Strong" else "❄️"

def emoji_risk(r):
    return "🟢" if r == "Tight" else "🟡" if r == "Moderate" else "🔴"

def emoji_conflict():
    return "⚠️"

def emoji_session(s):
    if s == "Asia":
        return "🌙"
    if s == "London":
        return "🌅"
    if s == "New York":
        return "🌆"
    return "⏳"

def emoji_volatility(v):
    return "🔥" if v == "High" else "🟡" if "Moderate" in v else "❄️"
