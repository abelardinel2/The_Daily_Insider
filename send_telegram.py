import requests
import os
from datetime import datetime, timedelta
import json

def send_summary(data):
    top_buys = float(data["top_buys"])
    top_sells = float(data["top_sells"])
    total_buys = float(data["total_buys"])
    total_sells = float(data["total_sells"])

    # Calculate the 5-day date range (mirroring fetcher.py's window)
    end_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0).strftime("%B %d, %Y")
    start_date = (datetime.today() - timedelta(days=5)).replace(hour=0, minute=0, second=0, microsecond=0).strftime("%B %d, %Y")
    date_range = f"{start_date}–{end_date}"  # e.g., "June 24–June 29, 2025"

    # If-then logic with ratio and fractional favor
    if total_buys + total_sells > 0:
        total_value = total_buys + total_sells
        if total_sells > total_buys and total_buys > 0:  # Avoid division by zero
            ratio = total_sells / total_buys
            if ratio > 10000:
                dominance_label = 'Overwhelming Sell Dominance'
                favor_denominator = min(round(ratio), 100)  # Cap at 100 for readability
                favor_text = f"1 in {favor_denominator} favors buy"
            elif ratio > 100:
                dominance_label = 'Strong Sell Dominance'
                favor_denominator = round(ratio)
                favor_text = f"1 in {favor_denominator} favors buy"
            else:
                dominance_label = 'Mild Sell Dominance'
                favor_denominator = round(ratio)
                favor_text = f"1 in {favor_denominator} favors buy"
        elif total_buys > total_sells and total_sells > 0:
            ratio = total_buys / total_sells
            if ratio > 10000:
                dominance_label = 'Overwhelming Buy Dominance'
                favor_denominator = min(round(ratio), 100)
                favor_text = f"1 in {favor_denominator} favors sell"
            elif ratio > 100:
                dominance_label = 'Strong Buy Dominance'
                favor_denominator = round(ratio)
                favor_text = f"1 in {favor_denominator} favors sell"
            else:
                dominance_label = 'Mild Buy Dominance'
                favor_denominator = round(ratio)
                favor_text = f"1 in {favor_denominator} favors sell"
        else:
            dominance_label = 'Balanced Market'
            favor_text = "1 in 1 favors both"
    else:
        dominance_label = 'No Data'
        favor_text = 'N/A'

    bias_detail = f'{dominance_label} ({favor_text}) 👀'

    # Format the message with consistent decimals
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