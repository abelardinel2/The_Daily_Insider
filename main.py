import os
from parse_form4 import get_recent_form4_amounts
from telegram_bot import send_telegram_message
from datetime import datetime

def main():
    company = os.getenv("COMPANY_NAME")
    sec_email = os.getenv("SEC_EMAIL")
    if not company or not sec_email:
        raise ValueError("COMPANY_NAME and SEC_EMAIL are required")

    label = os.getenv("SUMMARY_LABEL", "Morning")
    tickers = [
        "AAPL", "TSLA", "NVDA", "MSFT", "AMZN", "AMD", "META", "GOOG",
        "NFLX", "BRK.B", "JNJ", "UNH", "PG", "HD", "DIS", "MCD", "SBUX",
        "PEP", "KO", "WMT", "CVX", "V", "MA", "PYPL", "INTC", "CSCO",
        "ORCL", "IBM", "CRM", "ADBE", "SQ", "SHOP", "NKE", "UPS", "FDX",
        "BA", "LMT", "CAT", "GE", "LOW", "T", "VZ", "PFE", "MRK", "ABBV",
        "TMO", "BMY", "GILD", "VRTX", "AMGN"
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

    message = (
        f"📊 Insider Flow Summary – {today} ({label})\n\n"
        f"💰 Top Buys: ${total_buys * 1_000_000:,}\n"
        f"💥 Top Sells: ${total_sells * 1_000_000:,}\n\n"
        f"🧮 Total Buys: ${total_buys:.1f}M | Total Sells: ${total_sells:.1f}M\n"
        f"📉 Bias: {bias}"
    )

    send_telegram_message(message)

if __name__ == "__main__":
    main()