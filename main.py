import os
from sec_edgar_downloader import Downloader
from telegram_bot import send_telegram_message
from datetime import datetime
from collections import defaultdict

# NEW: Map for tricky tickers
ticker_map = {
    "BRK.B": "BRK-B",
    "BF.B": "BF-B",
    "GOOG.L": "GOOG",
    "RDS.A": "RDSA",
    "SHOP.TO": "SHOP",
    "BABA.HK": "BABA"
}

skipped = []

# Load tickers
with open("tickers.txt") as f:
    tickers = [line.strip() for line in f]

email = os.getenv("SEC_EMAIL")
dl = Downloader("Your Company Name", email)

buy_data = defaultdict(int)
sell_data = defaultdict(int)

for ticker in tickers:
    mapped = ticker_map.get(ticker, ticker)
    try:
        dl.get("4", mapped)
        # Your parse logic here...
    except Exception as e:
        skipped.append(mapped)
        continue

# Create your summary as usual...
summary = "📊 Insider Flow Summary – " + datetime.today().strftime("%B %d, %Y")

# Add skipped tickers to the end
if skipped:
    summary += f"\n⚠️ Skipped tickers: {', '.join(skipped)}"

send_telegram_message(summary)