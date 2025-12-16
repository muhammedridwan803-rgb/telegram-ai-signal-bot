import os
import base64
import requests

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "openai/gpt-4o"


def analyze_chart_image(image_bytes: bytes, context: dict) -> str:
    image_b64 = base64.b64encode(image_bytes).decode()

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a professional institutional trader. "
                    "You combine live market data, multi-timeframe structure, "
                    "and visual chart analysis.\n\n"
                    "STRICT RULES:\n"
                    "- NO buy/sell signals\n"
                    "- NO entries, TP, or SL\n"
                    "- Use POI language only (interest, reaction, rejection)\n"
                    "- Mention BOS / CHOCH only if visually apparent\n"
                    "- Numeric confidence score required\n"
                    "- Be concise, professional, trader-like\n"
                ),
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Context (from live data):\n"
                            f"Price: {context.get('price')}\n"
                            f"HTF Bias: {context.get('htf')}\n"
                            f"LTF Bias: {context.get('ltf')}\n"
                            f"EMA Trend: {context.get('ema')}\n"
                            f"RSI: {context.get('rsi')} ({context.get('rsi_state')})\n"
                            f"Session: {context.get('session')}\n\n"
                            "Analyze the chart visually and respond in THIS FORMAT ONLY:\n\n"
                            "💰 Price Context:\n"
                            "🕰 Timeframe Bias (HTF/LTF):\n"
                            "📈 Trend & Momentum:\n"
                            "🧱 POIs (HTF + LTF):\n"
                            "🔄 Structure (BOS / CHOCH if visible):\n"
                            "🔐 Confidence Score (%):\n"
                            "🧠 AI Insight (2–4 sentences):\n\n"
                            "End with: ℹ️ Analysis only — not a trade signal."
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_b64}"
                        },
                    },
                ],
            },
        ],
        "temperature": 0.3,
        "max_tokens": 600,
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30,
        )
        data = r.json()

        if "choices" not in data:
            return "⚠️ Analysis unavailable. Try a clearer chart."

        return data["choices"][0]["message"]["content"]

    except Exception:
        return "⚠️ Analysis failed. Please try again."
