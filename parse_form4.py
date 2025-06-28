import requests
from bs4 import BeautifulSoup

def parse_form4_xml(xml_url):
    resp = requests.get(xml_url, headers={"User-Agent": "OriaDawnBot"})
    if resp.status_code != 200:
        return {"buys": 0, "sells": 0}
    soup = BeautifulSoup(resp.text, "xml")

    buys = 0
    sells = 0

    for txn in soup.find_all("nonDerivativeTransaction"):
        code = txn.transactionAcquiredDisposedCode.value.text.strip()
        amount_node = txn.transactionShares.value
        amount = int(float(amount_node.text.strip())) if amount_node else 0
        if code == "A":
            buys += amount
        elif code == "D":
            sells += amount

    return {"buys": buys, "sells": sells}