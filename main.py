import os
from parse_form4 import parse_form4_amount
from telegram_bot import send_telegram_message
from datetime import datetime

def main():
    company = os.getenv("COMPANY_NAME")
    sec_email = os.getenv("SEC_EMAIL")

    if not company or not sec_email:
        raise ValueError("COMPANY_NAME and SEC_EMAIL must be set!")

    test_url = "https://www.sec.gov/Archives/edgar/data/1853513/000095017025091161/xslF345X03/ownership.xml"

    try:
        result = parse_form4_amount(test_url)
        buys = result["buys"]
        sells = result["sells"]

        bias = "Neutral Bias 👀"
        if buys > sells:
            bias = "Buy-Side Bias 👀"
        elif sells > buys:
            bias = "Sell-Side Bias 👀"

        today = datetime.today().strftime("%Y-%m-%d")
        message = (
            f"📊 Insider Flow Summary – {today} (Morning)\n\n"
            f"💰 Top Buys: ${buys}\n"
            f"💥 Top Sells: ${sells}\n\n"
            f"🧮 Total Buys: ${buys:.1f} | Total Sells: ${sells:.1f}\n"
            f"📉 Bias: {bias}"
        )
        send_telegram_message(message)

    except Exception as e:
        send_telegram_message(f"❌ Bot Error: {e}")

if __name__ == "__main__":
    main()