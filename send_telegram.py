import json
import requests
import os
import sys

def main():
    # 1. Load JSON
    with open("insider_flow.json") as f:
        data = json.load(f)

    top_buys = data.get("top_buys", 0)
    top_sells = data.get("top_sells", 0)
    total_buys = data.get("total_buys", 0)
    total_sells = data.get("total_sells", 0)

    # 2. Compute bias
    if total_buys > total_sells:
        bias = "Buy-Side Bias 👀"
    elif total_sells > total_buys:
        bias = "Sell-Side Bias 👀"
    else:
        bias = "Neutral Bias 👀"

    # 3. Format message
    message = f"""
📊 Insider Flow Summary

💰 Top Buys: ${top_buys:,}
💥 Top Sells: ${top_sells:,}

🧮 Total Buys: ${total_buys:,} | Total Sells: ${total_sells:,}
📉 Bias: {bias}
""".strip()

    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    if not BOT_TOKEN or not CHAT_ID:
        print("❌ Missing Telegram credentials! BOT_TOKEN or CHAT_ID is empty.")
        sys.exit(1)

    # 4. Build URL & payload
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}

    print(f"📨 Sending to Telegram: {url}")
    print(f"➡️ Payload: {payload}")

    # 5. Send it
    resp = requests.post(url, json=payload)
    try:
        resp.raise_for_status()
        print("✅ Telegram message sent successfully!")
    except Exception as e:
        print(f"❌ Telegram API error: {resp.status_code} {resp.text}")
        sys.exit(1)

if __name__ == "__main__":
    main()