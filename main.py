import os
from datetime import datetime, timedelta
from parse_form4 import get_recent_form4_amounts
from telegram_bot import send_telegram_message

def main():
    email = os.getenv("SEC_EMAIL")
    label = "Morning"
    today = datetime.today()
    start_date = (today - timedelta(days=30)).strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")

    with open("tickers.txt") as f:
        tickers = [line.strip() for line in f if line.strip()]

    total_buys = 0
    total_sells = 0

    for ticker in tickers:
        amounts = get_recent_form4_amounts(ticker, email, start_date, end_date)
        total_buys += amounts.get("buys", 0)
        total_sells += amounts.get("sells", 0)

    bias = "Neutral Bias 👀"
    if total_buys > total_sells:
        bias = "Buy-Side Bias 👀"
    elif total_sells > total_buys:
        bias = "Sell-Side Bias 👀"

    summary = f"""📊 Insider Flow Summary – {end_date} ({label})

💰 Top Buys: ${total_buys}
💥 Top Sells: ${total_sells}

🧮 Total Buys: ${total_buys:.1f}M | Total Sells: ${total_sells:.1f}M
📉 Bias: {bias}
"""
    send_telegram_message(summary)

if __name__ == "__main__":
    main()