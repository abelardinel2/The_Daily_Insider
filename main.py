import os
from sec_edgar_downloader import Downloader
from telegram_bot import send_telegram_message
from datetime import datetime
from collections import defaultdict
from parse_form4 import parse_amount_from_txt

# === NEW: Map odd tickers ===
def map_ticker(ticker):
    # Example: map BRK.B to BRK-B for CIK lookup
    if ticker.upper() == "BRK.B":
        return "BRK-B"
    return ticker

def get_summary():
    email = os.getenv("SEC_EMAIL")
    if not email:
        raise ValueError("Missing SEC_EMAIL environment variable")

    label = os.getenv("SUMMARY_LABEL", "Morning")
    date_label = datetime.today().strftime("%B %d, %Y")

    dl = Downloader("insider_flow", email)

    # Read tickers from file
    with open("tickers.txt", "r") as f:
        tickers = [line.strip() for line in f.readlines() if line.strip()]

    buy_data = defaultdict(int)
    sell_data = defaultdict(int)
    skipped = []

    for ticker in tickers:
        mapped = map_ticker(ticker)
        try:
            dl.get("4", mapped)
            folder = f"insider_flow/sec-edgar-filings/{mapped}/4/"
            if not os.path.exists(folder):
                skipped.append(ticker)
                continue
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.endswith(".txt"):
                        action = parse_amount_from_txt(os.path.join(root, file))
                        if action == 'buy':
                            buy_data[ticker] += 1_000_000
                        elif action == 'sell':
                            sell_data[ticker] += 1_000_000
        except Exception:
            skipped.append(ticker)

    top_buys = sorted(buy_data.items(), key=lambda x: x[1], reverse=True)[:3]
    top_sells = sorted(sell_data.items(), key=lambda x: x[1], reverse=True)[:3]
    total_buys = sum(buy_data.values())
    total_sells = sum(sell_data.values())

    if total_sells > total_buys:
        bias = "Sell-Side Bias"
    elif total_buys > total_sells:
        bias = "Buy-Side Bias"
    else:
        bias = "Neutral Bias"

    summary = f"""📊 Insider Flow Summary – {date_label} ({label})

💰 Top Buys
""" + "\n".join([f"{t} – ${v:,}" for t, v in top_buys]) + """

💥 Top Sells
""" + "\n".join([f"{t} – ${v:,}" for t, v in top_sells]) + f"""

🧮 Total Buys: ${total_buys/1e6:.1f}M | Total Sells: ${total_sells/1e6:.1f}M  
📉 Bias: {bias} 👀
"""

    if skipped:
        summary += "\n⚠️ Skipped tickers: " + ", ".join(skipped)

    return summary

if __name__ == "__main__":
    try:
        summary = get_summary()
        send_telegram_message(summary)
    except Exception as e:
        send_telegram_message(f"❌ Bot Error: {e}")