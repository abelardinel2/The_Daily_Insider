import requests
from bs4 import BeautifulSoup

def parse_form4_amount(filing_url):
    resp = requests.get(filing_url)
    if resp.status_code != 200:
        raise ValueError(f"Could not fetch XML: {resp.status_code}")

    soup = BeautifulSoup(resp.text, "xml")
    if soup.find("html"):
        raise ValueError("Expected XML but got HTML instead.")

    buys = 0
    sells = 0

    for txn in soup.find_all("nonDerivativeTransaction"):
        code = txn.transactionAcquiredDisposedCode.value.text
        shares = txn.transactionShares.value.text
        shares = float(shares)
        if code == "A":
            buys += shares
        elif code == "D":
            sells += shares

    return {"buys": buys, "sells": sells}