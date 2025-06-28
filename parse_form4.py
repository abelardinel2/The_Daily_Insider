from bs4 import BeautifulSoup
import requests
import os

SEC_EMAIL = os.getenv("SEC_EMAIL")
TEST_XML = "https://www.sec.gov/Archives/edgar/data/1853513/000095017025091161/xslF345X03/ownership.xml"

def parse_test_xml():
    headers = {
        "User-Agent": f"Oria Dawn Bot ({SEC_EMAIL})"
    }
    resp = requests.get(TEST_XML, headers=headers)
    if resp.status_code != 200:
        raise Exception(f"Could not fetch XML: {resp.status_code}")

    soup = BeautifulSoup(resp.text, "lxml-xml")

    # More robust: finds normal & derivative nodes
    codes = soup.find_all(["transactionAcquiredDisposedCode", "derivativeTransactionAcquiredDisposedCode"])

    buys = sum(1 for c in codes if c.text.strip().upper() == "A")
    sells = sum(1 for c in codes if c.text.strip().upper() == "D")

    summary = f"""
📊 Insider Flow Summary – Direct XML Test (Improved)

💰 Buys found: {buys}
💥 Sells found: {sells}

🧮 Total: Buys {buys} | Sells {sells}
"""
    return summary.strip()