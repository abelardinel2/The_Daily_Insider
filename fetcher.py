urls = [
    "https://www.sec.gov/Archives/edgar/data/1930021/000147450625000122/xslF345X03/primary_doc.xml"
]

def parse_form4_xml(url: str) -> dict:
    headers = {
        "User-Agent": "AmeliaBelardinelli (ameliabelardinelli@gmail.com)"
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise Exception(f"Failed to fetch {url} (Status: {resp.status_code})")

    soup = BeautifulSoup(resp.text, "xml")

    buys = 0
    sells = 0

    for txn in soup.find_all("nonDerivativeTransaction"):
        code = txn.transactionCode.string if txn.transactionCode else ""
        acquired_or_disposed = txn.transactionAcquiredDisposedCode.string if txn.transactionAcquiredDisposedCode else ""

        amount_node = txn.find("transactionShares")
        amount = float(amount_node.value.string) if amount_node and amount_node.value else 0

        if code == "P" or acquired_or_disposed == "A":
            buys += amount
        elif code == "S" or acquired_or_disposed == "D":
            sells += amount

    return {"buys": buys, "sells": sells}