import requests
from bs4 import BeautifulSoup

def parse_form4_xml(xml_url):
    resp = requests.get(xml_url)
    if resp.status_code != 200:
        raise Exception(f"Failed to get XML: {xml_url}")

    soup = BeautifulSoup(resp.text, "xml")

    buys = 0
    sells = 0

    for txn in soup.find_all("nonDerivativeTransaction"):
        code = txn.find("transactionAcquiredDisposedCode").get_text(strip=True)
        shares = float(txn.find("transactionShares").get_text(strip=True))
        price = float(txn.find("transactionPricePerShare").get_text(strip=True))
        amount = shares * price
        if code == "A":
            buys += amount
        elif code == "D":
            sells += amount

    for txn in soup.find_all("derivativeTransaction"):
        code = txn.find("transactionAcquiredDisposedCode").get_text(strip=True)
        shares = float(txn.find("transactionShares").get_text(strip=True))
        price = float(txn.find("transactionPricePerShare").get_text(strip=True))
        amount = shares * price
        if code == "A":
            buys += amount
        elif code == "D":
            sells += amount

    return {"buys": buys, "sells": sells}