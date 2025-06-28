import os
from datetime import datetime, timedelta
from parse_form4 import get_recent_form4_amounts
from telegram_bot import send_telegram_message

def main():
    company = os.getenv("COMPANY_NAME")
    sec_email = os.getenv("SEC_EMAIL")
    if not company or not sec_email:
        raise ValueError("COMPANY_NAME and SEC_EMAIL must be set!")

    label = os.getenv("SUMMARY_LABEL", "Morning")
    days_back = 5  # Rolling window

    tickers = ["GETY", "HOVR", "MCW"]  # Test tickers

    total_buys = 0
    total_sells = 0

    for ticker in tickers:
        try:
            print(f"Processing {ticker}...")
            amounts = get_recent_form4_amounts(ticker, sec_email, days_back)
            total_buys += amounts["buys"]
            total_sells += amounts["sells"]
        except Exception as e:
            send_telegram_message(f"❌ Bot Error for {ticker}: {e}")

    bias = "Neutral Bias 👀"
    if total_buys > total_sells:
        bias = "Buy-Side Bias 👀"
    elif total_sells > total_buys:
        bias = "Sell-Side Bias 👀"

    date_label = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")

    summary = f"""📊 Insider Flow Summary – {date_label} ({label})

💰 Top Buys: ${total_buys:,.0f}
💥 Top Sells: ${total_sells:,.0f}

🧮 Total Buys: ${total_buys/1e6:.1f}M | Total Sells: ${total_sells/1e6:.1f}M
📉 Bias: {bias}
"""
    send_telegram_message(summary)

if __name__ == "__main__":
    main()