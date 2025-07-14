import os
import requests

def send_telegram_alert(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("Missing Telegram credentials.")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "disable_web_page_preview": True}
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print("Telegram error:", response.text)
    except Exception as e:
        print("Telegram request failed:", e)