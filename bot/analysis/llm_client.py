import requests
from bot.core.config import OPENROUTER_API_KEY, OPENROUTER_URL, OPENROUTER_MODEL


def llm_explain(prompt):
    if not OPENROUTER_API_KEY:
        return None

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://localhost",
        "X-Title": "Telegram AI Market Bot"
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a professional market analyst. Be concise, neutral, and technical."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.4,
        "max_tokens": 160
    }

    try:
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=15
        )
        return r.json()["choices"][0]["message"]["content"]
    except Exception:
        return None
