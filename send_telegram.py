import os
import requests
import json
from datetime import datetime, timedelta

def send_summary(data):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")  # Existing secret
    chat_id = os.getenv("TELEGRAM_CHAT_ID")      # Existing secret
    print(f"Token: {bot_token[:5]}..., Chat ID: {chat_id}")  # Debug: Mask token
    if not bot_token or not chat_id:
        print("❌ Insider Flow Analyzer bot credentials missing")
        return

    total_trades = data.get("total_buys", 0) + data.get("total_sells", 0)
    buy_ratio = (data.get("total_buys", 0) / total_trades * 100) if total_trades else 0
    sell_ratio = (data.get("total_sells", 0) / total_trades * 100) if total_trades else 0
    sentiment = "Neutral"
    if buy_ratio > 60:
        sentiment = "Bullish"
    elif sell_ratio > 60:
        sentiment = "Bearish"

    message = f"📊 Insider Flow Summary (Analytics) ({datetime.now().strftime('%B %d, %Y')}–{datetime.now().strftime('%B %d, %Y')})\n\n"
    message += f"💰 Top Buys: ${data.get('top_buys', 0):,.2f}\n"
    message += f"💥 Top Sells: ${data.get('top_sells', 0):,.2f}\n\n"
    message += f"🧮 Total Buys: ${data.get('total_buys', 0):,.2f} | Total Sells: ${data.get('total_sells', 0):,.2f}\n"
    message += f"📈 Sentiment: {sentiment} ({buy_ratio:.2f}% buy, {sell_ratio:.2f}% sell) 👀"

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    response = requests.post(url, json={"chat_id": chat_id, "text": message})
    print(f"Response: {response.status_code} - {response.text}")  # Debug API response
    if response.status_code != 200:
        print(f"❌ Failed to send Analyzer message: {response.text}")
    else:
        print("✅ Analyzer message sent successfully!")

if __name__ == "__main__":
    try:
        with open("insider_flow.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ insider_flow.json not found")
        return
    except json.JSONDecodeError:
        print("❌ Invalid JSON in insider_flow.json")
        return
    send_summary(data)