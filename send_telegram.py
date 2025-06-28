import requests
import os

def send_summary(message: str):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not bot_token or not chat_id:
        raise ValueError("Missing Telegram env vars")

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}

    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    print("✅ Telegram message sent!")