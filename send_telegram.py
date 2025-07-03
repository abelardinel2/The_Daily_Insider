import os
import requests
from datetime import datetime

def send_summary(data):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not bot_token or not chat_id:
        print("❌ Analyzer bot credentials missing")
        return

    message = f"📊 Insider Flow Analyzer Summary ({datetime.now().strftime('%Y-%m-%d %H:%M:%S ET')})\n\n"
    message += f"Total Buys: {data.get('total_buys', 0):.2f}\n"
    message += f"Total Sells: {data.get('total_sells', 0):.2f}\n"
    message += f"Top Buys: {data.get('top_buys', 0):.2f}\n"
    message += f"Top Sells: {data.get('top_sells', 0):.2f}\n"
    if data.get('total_buys', 0) == 0 and data.get('total_sells', 0) == 0:
        message += "No significant insider activity detected.\n"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    response = requests.post(url, json={"chat_id": chat_id, "text": message})
    if response.status_code != 200:
        print(f"❌ Failed to send Analyzer message: {response.text}")
    else:
        print("✅ Analyzer message sent successfully!")

if __name__ == "__main__":
    with open("insider_flow_analyzer.json", "r") as f:
        data = json.load(f)
    send_summary(data)