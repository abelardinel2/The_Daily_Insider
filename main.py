import os
import requests

def send_telegram_message(message):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not bot_token or not chat_id:
        raise ValueError("Telegram credentials missing.")

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    response = requests.post(url, data=payload)
    print(f"Sent to Telegram. Status: {response.status_code}, Response: {response.text}")

    if response.status_code != 200:
        raise Exception(f"Telegram error: {response.text}")