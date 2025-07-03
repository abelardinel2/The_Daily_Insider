import os
import requests
from datetime import datetime, timedelta

def send_summary(data):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")  # Existing secret
    chat_id = os.getenv("TELEGRAM_CHAT_ID")      # Existing secret
    if not bot_token or not chat_id:
        print("❌ Insider Flow Analyzer bot credentials missing")
        return

    total_trades = data["total_buys"] + data["total_sells"]
    buy_ratio = (data["total_buys"] / total_trades * 100) if total_trades else 0
    sell_ratio = (data["total_sells"] / total_trades * 100) if total_trades else 0
    sentiment = "Neutral"
    if buy_ratio > 60:
        sentiment = "Bullish"
    elif sell_ratio > 60:
        sentiment = "Bearish"

    message = f"📊 Insider Flow Summary (Analytics) ({datetime.now().strftime('%B %d, %Y')}–{datetime.now().strftime('%B %d, %Y')})\n\n"
    message += f"💰 Top Buys: ${data['top_buys']:,.2f}\n"
    message += f"💥 Top Sells: ${data['top_sells']:,.2f}\n\n"
    message += f"🧮 Total Buys: ${data['total_buys']:,.2f} | Total Sells: ${data['total_sells']:,.2f}\n"
    message += f"📈 Sentiment: {sentiment} ({buy_ratio:.2f}% buy, {sell_ratio:.2f}% sell) 👀"

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    response = requests.post(url, json={"chat_id": chat_id, "text": message})
    if response.status_code != 200:
        print(f"❌ Failed to send Analyzer message: {response.text}")
    else:
        print("✅ Analyzer message sent successfully!")

if __name__ == "__main__":
    with open("insider_flow.json", "r") as f:
        data = json.load(f)
    send_summary(data)