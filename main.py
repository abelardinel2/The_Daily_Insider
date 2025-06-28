import os
from telegram_bot import send_telegram_message
from parse_form4 import get_recent_form4_amounts
from datetime import datetime

TICKERS = ["AAPL", "TSLA", "NVDA"]  # Example test tickers

def summarize_insider_flows():
    email = os.getenv("SEC_EMAIL")
    label = os.getenv("SUMMARY_LABEL", "Morning")
    today = datetime.today().strftime("%Y-%m-%d")

    total_buys = 0
    total_sells = 0

    for ticker in TICKERS:
        amounts = get_recent_form4_amounts(ticker, email)
        total_buys += amounts['buys']
        total_sells += amounts['sells']

    summary = f"""📊 Insider Flow Summary – {today} ({label})

💰 Top Buys: ${total_buys:,.0f}
💥 Top Sells: ${total_sells:,.0f}

🧮 Total Buys: ${total_buys/1e6:.1f}M | Total Sells: ${total_sells/1e6:.1f}M
📉 Bias: {"Buy-Side Bias 👀" if total_buys > total_sells else "Sell-Side Bias 👀" if total_sells > total_buys else "Neutral Bias 👀"}
"""
    send_telegram_message(summary)

if __name__ == "__main__":
    summarize_insider_flows()