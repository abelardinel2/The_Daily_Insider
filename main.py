import os
from datetime import datetime, timedelta
from parse_form4 import parse_form4_amount
from telegram_bot import send_telegram_message

# Logging for debug
import logging
logging.basicConfig(level=logging.INFO)

def main():
    tickers = []
    with open("tickers.txt") as f:
        tickers = [line.strip() for line in f if line.strip()]

    company_name = os.getenv("COMPANY_NAME")
    sec_email = os.getenv("SEC_EMAIL")

    total_buys = 0
    total_sells = 0

    # Rolling date range: last 5 days
    today = datetime.utcnow().date()
    five_days_ago = today - timedelta(days=5)

    for ticker in tickers:
        try:
            amounts = parse_form4_amount(ticker, sec_email, five_days_ago, today)
            total_buys += amounts["buys"]
            total_sells += amounts["sells"]
        except Exception as e:
            logging.warning(f"Issue with {ticker}: {e}")

    bias = "Neutral Bias 👀"
    if total_buys > total_sells:
        bias = "Buy-Side Bias 👀"
    elif total_sells > total_buys:
        bias = "Sell-Side Bias 👀"

    summary = f"""📊 Insider Flow Summary – {today} (Morning)

💰 Top Buys: ${total_buys:,.0f}
💥 Top Sells: ${total_sells:,.0f}

🧮 Total Buys: ${total_buys/1e6:.1f}M | Total Sells: ${total_sells/1e6:.1f}M
📉 Bias: {bias}"""

    send_telegram_message(summary)

if __name__ == "__main__":
    main()