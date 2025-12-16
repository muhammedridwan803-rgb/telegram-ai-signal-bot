from bot.analysis.structure import detect_structure
from bot.analysis.zones import detect_zones


def evaluate_setup(df, indicators):
    if df is None or not indicators:
        return {}

    structure_data = detect_structure(df)
    zones = detect_zones(df)

    swing_high = structure_data.get("swing_high")
    swing_low = structure_data.get("swing_low")
    price = float(df["close"].iloc[-1])

    equilibrium = (swing_high + swing_low) / 2 if swing_high and swing_low else None
    location = "Discount" if equilibrium and price < equilibrium else "Premium"

    # ---------------- QUALITY SCORE ----------------
    quality = 0

    if structure_data.get("structure") == indicators.get("trend"):
        quality += 40
    else:
        quality += 20

    if zones:
        quality += 30

    if indicators.get("macd") == indicators.get("trend"):
        quality += 20
    else:
        quality += 10

    if indicators.get("volume") == "High":
        quality += 10

    if quality >= 70:
        quality_label = "High"
    elif quality >= 40:
        quality_label = "Moderate"
    else:
        quality_label = "Weak"

    # ---------------- CONFIDENCE SCORE ----------------
    confidence = 0

    if structure_data.get("structure") == indicators.get("trend"):
        confidence += 35
    else:
        confidence += 18

    if zones:
        confidence += 30

    if indicators.get("macd") == indicators.get("trend"):
        confidence += 20
    else:
        confidence += 10

    if indicators.get("volume") == "High":
        confidence += 15
    elif indicators.get("volume") == "Normal":
        confidence += 8

    if confidence >= 80:
        confidence_label = "High"
    elif confidence >= 55:
        confidence_label = "Moderate"
    else:
        confidence_label = "Low"

    # ---------------- STATUS ----------------
    status = "Forming"
    if zones:
        z = zones[0]
        if z["low"] <= price <= z["high"]:
            status = "Active"
        elif price < z["low"] and z["type"] == "Demand":
            status = "Invalidated"
        elif price > z["high"] and z["type"] == "Supply":
            status = "Invalidated"

    # ---------------- TRADE FRAMEWORK (IDEAS) ----------------
    framework = {}
    if zones:
        z = zones[0]
        if z["type"] == "Demand":
            framework = {
                "bias": "Long idea (reaction-based)",
                "entry_zone": f"{z['low']} – {z['high']}",
                "invalidation": f"Below {z['low']}",
                "target": "Previous swing high / equilibrium"
            }
        else:
            framework = {
                "bias": "Short idea (reaction-based)",
                "entry_zone": f"{z['low']} – {z['high']}",
                "invalidation": f"Above {z['high']}",
                "target": "Previous swing low / equilibrium"
            }

    return {
        "current_price": price,
        "structure": structure_data.get("structure"),
        "price_location": location,
        "quality_score": quality,
        "quality_label": quality_label,
        "confidence_score": confidence,
        "confidence_label": confidence_label,
        "status": status,
        "zones": zones,
        "framework": framework
    }
