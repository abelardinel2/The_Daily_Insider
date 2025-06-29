import requests
import os
from datetime import datetime, timedelta

def send_summary(data):
    top_buys = data["top_buys"]
    top_sells = data["top_sells"]
    total_buys = data["total_buys"]
    total_sells = data["total_sells"]

    # Calculate the 5-day date range (mirroring fetcher.py's window)
    end_date = datetime.today().strftime("%B %d, %Y")
    start_date = (datetime.today() - timedelta(days=5)).strftime("%B %d, %Y")
    date_range = f"{start_date}–{end_date}"  # e.g., "June 23–June 28, 2025"

    # Calculate bias percentages
    total_value = total_buys + total_sells if total_buys + total_sells > 0 else 1  # Avoid division by zero
    buy_pct = (total_buys / total_value * 100) if total_value > 0 else 0
    sell_pct = (total_sells / total_value * 100) if total_value > 0 else 0
    bias_label = "Neutral Bias" if abs(buy_pct - sell_pct) < 1 else ("Buy-Side Bias" if buy_pct > sell_pct else "Sell-Side Bias")
    bias_detail = f"{bias_label} ({sell_pct:.2f}% sell, {buy_pct:.2f}% buy) 👀"

    # Format the message with consistent decimals and enhancements
    message = f"""
📊 Insider Flow Summary ({date_range})

💰 Top Buys: ${top_buys:,.2f}
💥 Top Sells: ${top_sells:,.2f}

🧮 Total Buys: ${total_buys:,.2f} | Total Sells: ${total_sells:,.2f}
📉 {bias_detail}
"""

    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}

    resp = requests.post(url, json=payload)
    resp.raise_for_status()

    print("✅ Telegram message sent!")

if __name__ == "__main__":
    with open("insider_flow.json", "r") as f:
        data = json.load(f)
    send_summary(data)