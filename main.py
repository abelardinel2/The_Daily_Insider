import os
from sec_edgar_downloader import Downloader
from telegram_bot import send_telegram_message
from datetime import datetime
from collections import defaultdict

def parse_amount_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read().lower()
        if 'acquired' in text:
            return 'buy'
        elif 'disposed' in text:
            return 'sell'
    return 'unknown'

def get_summary():
    email = os.getenv("SEC_EMAIL")
    if not email:
        raise ValueError("Missing SEC_EMAIL environment variable")

    label = os.getenv("SUMMARY_LABEL", "Morning")
    today = datetime.today().strftime("%Y-%m-%d")
    date_label = datetime.today().strftime("%B %d, %Y")

    dl = Downloader("sec_data", email)

    tickers = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN", "AMD"]
    buy_data = defaultdict(int)
    sell_data = defaultdict(int)

    for ticker in tickers:
        dl.get("4", ticker)
        folder = f"sec_data/sec-edgar-filings/{ticker}/4/"
        if not os.path.exists(folder):
            continue
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith(".txt"):
                    action = parse_amount_from_txt(os.path.join(root, file))
                    if action == 'buy':
                        buy_data[ticker] += 1000000  # Placeholder value
                    elif action == 'sell':
                        sell_data[ticker] += 1000000

    top_buys = sorted(buy_data.items(), key=lambda x: x[1], reverse=True)[:3]
    top_sells = sorted(sell_data.items(), key=lambda x: x[1], reverse=True)[:3]
    total_buys = sum(buy_data.values())
    total_sells = sum(sell_data.values())

    if total_sells > total_buys:
        bias = "Moderate Sell-Side Bias"
    elif total_buys > total_sells:
        bias = "Buy-Side Bias"
    else:
        bias = "Neutral Bias"

    summary = f"""📊 Insider Flow Summary – {date_label} ({label})

💰 Top Buys
""" + "\n".join([f"${t} – ${v:,}" for t, v in top_buys]) + """

💥 Top Sells
""" + "\n".join([f"${t} – ${v:,}" for t, v in top_sells]) + f"""

🧮 Total Buys: ${total_buys/1e6:.1f}M | Total Sells: ${total_sells/1e6:.1f}M  
📉 Bias: {bias} 👀
"""
    return summary

if __name__ == "__main__":
    try:
        summary = get_summary()
        send_telegram_message(summary)
    except Exception as e:
        send_telegram_message(f"❌ Bot Error: {e}")