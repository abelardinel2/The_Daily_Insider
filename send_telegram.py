import os
import requests

def send_telegram_message(msg):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat:
        raise Exception("Missing Telegram config.")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    res = requests.post(url, data={"chat_id": chat, "text": msg})
    if res.status_code != 200:
        raise Exception(f"Telegram fail: {res.text}")
