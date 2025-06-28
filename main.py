import os
from telegram_bot import send_telegram_message
from sec_edgar_downloader import Downloader
from parse_form4 import parse_form4_amount
from datetime import datetime
from collections import defaultdict

def get_real_summary():
    email = os.getenv("SEC_EMAIL")
    if not email:
        raise ValueError("Missing SEC_EMAIL")

    today = datetime.today().strftime("%B %d, %Y")

    dl = Downloader("sec_data", email)

    buys = defaultdict(float)
    sells = defaultdict(float)

    with open("tickers.txt") as f:
        tickers = [line.strip() for line in f]

    for ticker in tickers:
        print(f"Processing {ticker}")
        # Simulate download
        dl.get("4", ticker)
        amount = parse_form4_amount(None)
        print(f"Parsed amount for {ticker}: {amount}")
        buys[ticker] += amount

    top_buys = sorted(buys.items(), key=lambda x: -x[1])[:5]

    message = f"📊 Insider Flow Summary – {today}\n\n💰 Top Buys\n"
    for t, v in top_buys:
        message += f"{t} – ${v:,}\n"

    send_telegram_message(message)

if __name__ == "__main__":
    get_real_summary()