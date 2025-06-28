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

    result = parse_form4_amount(test_url)

    buys = result["buys"]
    sells = result["sells"]

    message = (
        f"📊 Insider Flow Summary – {datetime.today().strftime('%Y-%m-%d')}\n\n"
        f"💰 Top Buys: {buys}\n"
        f"💥 Top Sells: {sells}\n\n"
        f"🧮 Total Buys: {buys} | Total Sells: {sells}\n"
    )

    send_telegram_message(message)

if __name__ == "__main__":
    main()