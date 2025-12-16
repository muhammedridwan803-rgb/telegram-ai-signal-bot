import os
from bot.core.bot import build_app


def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN not set")

    app = build_app(token)
    app.run_polling()


if __name__ == "__main__":
    main()
