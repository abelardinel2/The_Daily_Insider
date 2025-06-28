import os
from parse_form4 import parse_form4_amount
from telegram_bot import send_telegram_message

def main():
    # ✅ Known working SEC XML link (copy-paste EXACT)
    filing_url = "https://www.sec.gov/Archives/edgar/data/1853513/000095017025091161/xslF345X03/ownership.xml"
    
    print(f"Testing direct link: {filing_url}")

    try:
        amounts = parse_form4_amount(filing_url)
        message = f"✅ Direct test\nBuys: {amounts['buys']}\nSells: {amounts['sells']}"
        send_telegram_message(message)
    except Exception as e:
        send_telegram_message(f"❌ Bot Error: {e}")

if __name__ == "__main__":
    main()