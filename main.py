import os
from datetime import datetime
from parse_form4 import parse_form4_amount
from telegram_bot import send_telegram_message

def main():
    tickers = []
    with open("tickers.txt", "r") as f:
        tickers = [line.strip() for line in f.readlines() if line.strip()]

    buys = sells = 0

    for ticker in tickers:
        amount = parse_form4_amount(ticker)
        if amount > 0:
            buys += amount
        else:
            sells += abs(amount)

    bias = "Neutral Bias 👀"
    if buys > sells:
        bias = "Buy-Side Bias 👀"
    elif sells > buys:
        bias = "Sell-Side Bias 👀"

    summary = f"""📊 Insider Flow Summary – {datetime.today().strftime('%B %d, %Y')} (Morning)

💰 Top Buys: ${buys:,}
💥 Top Sells: ${sells:,}

🧮 Total Buys: ${buys/1e6:.1f}M | Total Sells: ${sells/1e6:.1f}M
📉 Bias: {bias}"""

    send_telegram_message(summary)

    with open("snapshot.txt", "w") as f:
        f.write(summary)

if __name__ == "__main__":
    main()