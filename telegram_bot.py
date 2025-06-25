import requests

# Your Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = "7975548444:AAFtmHs3S3GYL_rDpawtDE-f_09_lFg3ex8"
TELEGRAM_CHAT_ID = "6652085600"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=data)
    return response.status_code == 200
