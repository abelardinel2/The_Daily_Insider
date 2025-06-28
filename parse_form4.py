import requests
from bs4 import BeautifulSoup
import os

def parse_form4_amount(url):
    email = os.getenv("SEC_EMAIL")
    if not email:
        raise ValueError("SEC_EMAIL not set!")

    headers = {
        "User-Agent": f"{email} (InsiderFlowBot)"
    }

    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise ValueError(f"Could not fetch Form 4: {resp.status_code}")

    soup = BeautifulSoup(resp.content, "xml")
    if soup.find("html"):
        raise ValueError("Expected XML but got HTML instead.")

    buys = 0
    sells = 0

    for txn in soup.find_all("nonDerivativeTransaction"):
        code = txn.find("transactionAcquiredDisposedCode").get_text(strip=True)
        shares = txn.find("transactionShares").get_text(strip=True)
        shares = float(shares)

        if code == "A":
            buys += shares
        elif code == "D":
            sells += shares

    return {"buys": buys, "sells": sells}