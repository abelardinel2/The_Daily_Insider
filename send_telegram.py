import os
import requests

def send_telegram_message(message):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    resp = requests.post(url, data=payload)
    if resp.status_code == 200:
        print("✅ Message sent!")
    else:
        print(f"❌ Failed to send message: {resp.text}")