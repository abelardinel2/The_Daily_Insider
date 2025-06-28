import os
from parse_form4 import get_recent_form4_amounts
from telegram_bot import send_telegram_message
from datetime import datetime

def main():
    company = os.getenv("COMPANY_NAME")
    sec_email = os.getenv("SEC_EMAIL")
    if not company or not sec_email:
        raise ValueError("COMPANY_NAME and SEC_EMAIL must be set.")

    label = os.getenv("SUMMARY_LABEL", "Morning")

    # ✅ TEST TICKERS ONLY
    tickers = [
        "GETY",
        "HOVR",
        "MCW"
    ]

    total_buys = 0
    total_sells = 0

    for ticker in tickers:
        print(f"Processing {ticker}...")
        amounts = get_recent_form4_amounts(ticker, sec_email)
        total_buys += amounts["buys"]
        total_sells += amounts["sells"]

    bias = "Neutral"
    if total_buys > total_sells:
        bias = "Buy-Side Bias 👀"
    elif total_sells > total_buys:
        bias = "Sell-Side Bias 👀"

    today = datetime.today().strftime("%B %d, %Y")
    summary = f"""📊 Insider Flow Summary – {today} ({label})

💰 Top Buys: ${total_buys:,}
💥 Top Sells: ${total_sells:,}

🧮 Total Buys: ${total_buys/1e6:.1f}M | Total Sells: ${total_sells/1e6:.1f}M
📉 Bias: {bias}"""

    send_telegram_message(summary)

if __name__ == "__main__":
    main()