import os
from parse_form4 import parse_form4_amount
from telegram_bot import send_telegram_message

def main():
    test_url = "https://www.sec.gov/Archives/edgar/data/1853513/000095017025091161/xslF345X03/ownership.xml"
    result = parse_form4_amount(test_url)
    send_telegram_message(f"Test XML parsed: {result}")

if __name__ == "__main__":
    main()