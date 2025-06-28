import os
import requests
from bs4 import BeautifulSoup

from telegram_bot import send_telegram_message  # keep your working telegram_bot.py!

# === CONFIG ===
SEC_EMAIL = os.getenv("SEC_EMAIL")
TEST_XML = "https://www.sec.gov/Archives/edgar/data/1853513/000095017025091161/xslF345X03/ownership.xml"

# === Run ===
def parse_test_xml():
    headers = {
        "User-Agent": f"Oria Dawn Bot ({SEC_EMAIL})"
    }
    resp = requests.get(TEST_XML, headers=headers)
    if resp.status_code != 200:
        raise Exception(f"Could not fetch XML: {resp.status_code}")

    soup = BeautifulSoup(resp.text, "xml")
    codes = soup.find_all("transactionAcquiredDisposedCode")

    buys = sum(1 for c in codes if c.text == "A")
    sells = sum(1 for c in codes if c.text == "D")

    summary = f"""
📊 Insider Flow Summary – Direct XML Test

💰 Buys found: {buys}
💥 Sells found: {sells}

🧮 Total: Buys {buys} | Sells {sells}
"""
    return summary.strip()

if __name__ == "__main__":
    try:
        message = parse_test_xml()
        send_telegram_message(message)
    except Exception as e:
        send_telegram_message(f"❌ Test Error: {e}")