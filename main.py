import os
from sec_edgar_downloader import Downloader
from telegram_bot import send_telegram_message
from parse_form4 import parse_form4_xml
from datetime import datetime
from collections import defaultdict

def get_real_summary():
    email = os.getenv("SEC_EMAIL")
    if not email:
        raise ValueError("Missing SEC_EMAIL environment variable")

    label = os.getenv("SUMMARY_LABEL", "Morning")
    today = datetime.today().strftime("%B %d, %Y")

    dl = Downloader("sec_data", email)

    buys = defaultdict(float)
    sells = defaultdict(float)

    with open("tickers.txt") as f:
        tickers = [line.strip() for line in f if line.strip()]

    for ticker in tickers:
        dl.get("4", ticker)
        folder = f"sec_data/sec-edgar-filings/{ticker}/4/"
        for root, _, files in os.walk(folder):
            for file in files:
                if file.endswith(".xml"):
                    b, s = parse_form4_xml(os.path.join(root, file))
                    buys[ticker] += b
                    sells[ticker] += s

    top_buys = sorted(buys.items(), key=lambda x: x[1], reverse=True)[:3]
    top_sells = sorted(sells.items(), key=lambda x: x[1], reverse=True)[:3]

    total_buys = sum(buys.values())
    total_sells = sum(sells.values())

    if total_sells > total_buys:
        bias = "Moderate Sell-Side Bias"
    elif total_buys > total_sells:
        bias = "Buy-Side Bias"
    else:
        bias = "Neutral Bias"

    summary = f"""📊 Insider Flow Summary – {today} ({label})

💰 Top Buys
""" + "\n".join([f"{t} – ${v:,.0f}" for t, v in top_buys]) + """

💥 Top Sells
""" + "\n".join([f"{t} – ${v:,.0f}" for t, v in top_sells]) + f"""

🧮 Total Buys: ${total_buys/1e6:.1f}M | Total Sells: ${total_sells/1e6:.1f}M  
📉 Bias: {bias} 👀
"""
    return summary

if __name__ == "__main__":
    try:
        summary = get_real_summary()
        send_telegram_message(summary)
    except Exception as e:
        send_telegram_message(f"❌ Bot Error: {e}")