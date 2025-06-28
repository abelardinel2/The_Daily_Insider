import os
from parse_form4 import parse_form4_amount
from telegram_bot import send_telegram_message

def main():
    # ✅ Example test Form 4 URL — replace with your own or loop later
    filing_url = "https://www.sec.gov/Archives/edgar/data/1853513/000095017025091161/xslF345X03/ownership.xml"

    # Parse
    amounts = parse_form4_amount(filing_url)

    buys = amounts["buys"]
    sells = amounts["sells"]

    bias = "Neutral Bias"
    if buys > sells:
        bias = "Buy-Side Bias"
    elif sells > buys:
        bias = "Sell-Side Bias"

    summary = f"""📊 Insider Flow Summary – Test

💰 Top Buys: ${buys:,.2f}
💥 Top Sells: ${sells:,.2f}

🧮 Total Buys: ${buys/1e6:.1f}M | Total Sells: ${sells/1e6:.1f}M
📉 Bias: {bias} 👀
"""
    print(summary)

    # ✅ Send to Telegram too
    try:
        send_telegram_message(summary)
    except Exception as e:
        print(f"❌ Telegram failed: {e}")

if __name__ == "__main__":
    main()