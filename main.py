import os
import telegram
from datetime import datetime
from sec_edgar_downloader import Downloader

def get_summary():
    dl = Downloader("sec_data")
    today = datetime.today().strftime('%Y-%m-%d')
    filings = dl.get("4", amount=10)
    summary = f"📊 Insider Flow Summary – {today}\n\n"
    summary += "This is a placeholder summary. Real data parsing to be implemented.\n"
    return summary

def send_to_telegram(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        raise Exception("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in environment.")
    bot = telegram.Bot(token=token)
    bot.send_message(chat_id=chat_id, text=message)

if __name__ == "__main__":
    summary = get_summary()
    send_to_telegram(summary)
