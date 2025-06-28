import requests
from bs4 import BeautifulSoup

def parse_form4_xml(url: str) -> dict:
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception(f"Failed to fetch {url}")

    soup = BeautifulSoup(resp.text, "xml")

    buys = 0
    sells = 0

    for txn in soup.find_all("nonDerivativeTransaction"):
        code = txn.transactionCode.string if txn.transactionCode else ""
        amount_node = txn.find("transactionShares")
        amount = float(amount_node.value.string) if amount_node else 0

        if code == "P":   # Purchase
            buys += amount
        elif code == "S": # Sale
            sells += amount

    return {"buys": buys, "sells": sells}