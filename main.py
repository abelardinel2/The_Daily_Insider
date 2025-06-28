import os
from datetime import datetime
from send_telegram_message import send_telegram_message
from parse_form4 import parse_form4_amount
import time

def main():
    email = os.getenv("SEC_EMAIL")
    label = os.getenv("SUMMARY_LABEL", "Morning")

    with open("tickers.txt", "r") as f:
        tickers = [line.strip() for line in f if line.strip()]

    total_buys = 0
    total_sells = 0

    for ticker in tickers:
        result = parse_form4_amount(ticker, email)
        total_buys += result["buys"]
        total_sells += result["sells"]
        time.sleep(0.5)  # gentle delay for SEC

    today = datetime.today().strftime("%Y-%m-%d")

    summary = f"""📊 Insider Flow Summary – {today} ({label})

💰 Top Buys: ${total_buys:,}
💥 Top Sells: ${total_sells:,}

🧮 Total Buys: ${total_buys / 1e6:.1f}M | Total Sells: ${total_sells / 1e6:.1f}M
📉 Bias: {"Buy-Side Bias" if total_buys > total_sells else "Sell-Side Bias" if total_sells > total_buys else "Neutral Bias"} 👀
"""
    send_telegram_message(summary)

if __name__ == "__main__":
    main()