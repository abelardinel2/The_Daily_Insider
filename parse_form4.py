import requests
import xml.etree.ElementTree as ET

def parse_form4_amount(filing_url):
    resp = requests.get(filing_url)
    text = resp.text.strip()

    # ✅ Check that the file starts with XML tag
    if not text.startswith("<?xml"):
        raise ValueError("Invalid XML: Response does not start with <?xml ...")

    root = ET.fromstring(text)

    buys = 0.0
    sells = 0.0

    for txn in root.iter("nonDerivativeTransaction"):
        code = txn.findtext(".//transactionAcquiredDisposedCode/value")
        shares = txn.findtext(".//transactionShares/value")
        if shares:
            shares = float(shares)
            if code == "A":
                buys += shares
            elif code == "D":
                sells += shares

    return {"buys": buys, "sells": sells}