import os
import requests
import json

def send_message(message):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    resp = requests.post(url, data=payload)
    resp.raise_for_status()

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
    send_message(message)

if __name__ == "__main__":
    main()