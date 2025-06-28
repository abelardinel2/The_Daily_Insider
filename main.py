import json
import requests
import os

def main():
    with open("insider_flow.json") as f:
        data = json.load(f)

    top_buys = data["top_buys"]
    top_sells = data["top_sells"]
    total_buys = data["total_buys"]
    total_sells = data["total_sells"]

    bias = "Neutral Bias 👀"
    if total_buys > total_sells:
        bias = "Buy-Side Bias 👀"
    elif total_sells > total_buys:
        bias = "Sell-Side Bias 👀"

    message = f"""
📊 Insider Flow Summary

💰 Top Buys: ${top_buys:,}
💥 Top Sells: ${top_sells:,}

🧮 Total Buys: ${total_buys:,} | Total Sells: ${total_sells:,}
📉 Bias: {bias}
"""

    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}

    resp = requests.post(url, json=payload)

    if resp.status_code == 200:
        print("✅ Telegram message sent!")
    else:
        print(f"❌ Failed to send Telegram. Status: {resp.status_code}, Response: {resp.text}")
        resp.raise_for_status()

if __name__ == "__main__":
    main()