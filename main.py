import os
from sec_edgar_downloader import Downloader
from parse_form4 import parse_form4_amount
from telegram_bot import send_telegram_message
from datetime import datetime

# Load tickers
with open("tickers.txt") as f:
    tickers = [line.strip() for line in f if line.strip()]

# Optional: special CIK fallback
SPECIAL_TICKERS = {
    "BRK.B": "1067983",
    "BF.B": "10456"
}

# Env setup
COMPANY_NAME = os.getenv("COMPANY_NAME")
SEC_EMAIL = os.getenv("SEC_EMAIL")

if not COMPANY_NAME or not SEC_EMAIL:
    raise ValueError("COMPANY_NAME and SEC_EMAIL must be set")

dl = Downloader(COMPANY_NAME, SEC_EMAIL)

total_buys = 0
total_sells = 0

for ticker in tickers:
    try:
        cik = SPECIAL_TICKERS.get(ticker, dl.lookup_cik(ticker))
        dl.get("4", cik)
        amount = parse_form4_amount("dummy_path")
        if amount >= 0:
            total_buys += amount
        else:
            total_sells += abs(amount)
    except Exception as e:
        print(f"Skipped {ticker}: {e}")

summary = f"""
📊 Insider Flow Summary – {datetime.now().strftime('%B %d, %Y')} (Morning)

💰 Top Buys: ${total_buys:,}
💥 Top Sells: ${total_sells:,}

🧮 Total Buys: ${total_buys/1e6:.1f}M | Total Sells: ${total_sells/1e6:.1f}M
📉 Bias: {"Buy-Side Bias 👀" if total_buys > total_sells else "Sell-Side Bias 👀"}
"""

send_telegram_message(summary)